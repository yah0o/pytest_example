const plan = require('flightplan');

const appName = 'dummy-server';
const ds_startFile = 'start_dummy_server.js';
const ls_startFile = 'start_logging_server.js';
const username = 'ubuntu';
const tmpDir = `${appName}`;

plan.target('production', [
    {
        host: '34.217.73.245',
        username: username,
        agent: process.env.SSH_AUTH_SOCK,
    }
]);

plan.local((local) => {
    // run unit tests before deploying
    local.exec('npm test');
    
    // rsync files to all the destination's hosts
    local.log('Copy files to remote hosts');
    let filesToCopy = local.exec('git ls-files', {silent: false});
    local.transfer(filesToCopy, '/tmp/' + tmpDir);
});

plan.remote((remote) => {
    remote.log('Move folder to root');
    remote.sudo(`cp -R /tmp/${tmpDir} ~`, {user: username});
    remote.rm(`-r /tmp/${tmpDir}`);

    remote.log('Install dependencies');
    remote.sudo(`npm --production --prefix ~/${tmpDir} install ~/${tmpDir}`, {user: username});

    remote.log('Creating logs directory');
    remote.rm(`-r ~/${appName}/logs`, {failsafe: true});
    remote.mkdir(`~/${appName}/logs`);

    remote.log('Reload application');
    remote.exec('forever stopall');

    let dummy_server_out_file = `~/${appName}/logs/dummy_server_out-${Date.now()}.log`;
    let dummy_server_err_file = `~/${appName}/logs/dummy_server_err-${Date.now()}.log`;
    remote.exec(`forever start -o ${dummy_server_out_file} -e ${dummy_server_err_file} ~/${appName}/${ds_startFile}`);

    let logging_server_out_file = `~/${appName}/logs/logging_server_out-${Date.now()}.log`;
    let logging_server_err_file = `~/${appName}/logs/logging_server_err-${Date.now()}.log`;
    remote.exec(`forever start -o ${logging_server_out_file} -e ${logging_server_err_file} ~/${appName}/${ls_startFile}`);
});