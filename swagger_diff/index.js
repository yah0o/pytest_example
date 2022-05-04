const Swagger = require('./swagger.js');
const ArgumentParser = require('./argsparse.js');
const Util = require('util');
const Filesystem = require('fs');

/**
 * main
 */

args = new ArgumentParser();
args.addArgument('--old', 'string', 'url to swagger.json of the older version', true);
args.addArgument('--new', 'string', 'url to swagger.json of the newer version', true);
args.addArgument('--ignoreIds', 'json', 'ruleIds to Ignore', false, ['edit-description', 'edit-summary', 'add-description']);
args.parse();

let old_ = args.getArgument('--old');
let new_ = args.getArgument('--new');
let ignore = args.getArgument('--ignoreIds');

swagger = new Swagger();
swagger.once(Swagger.ON_WRITTEN, () => {
    console.log('done');
});

swagger.once(Swagger.ON_ERROR, message => {
    console.log(message);
    process.exit(1);
});

Filesystem.mkdir('results', (err) => {
    if (err) {
        if (err.code === 'EEXIST')
            console.log('directory exists');
        else
            console.log(err);
    }

    swagger.report(Util.format('results/result%s.html', Date.now()), old_, new_, ignore);
});
