const DummyServer = require('./dummy_server.js');

let port = process.env.hasOwnProperty('DUMMY_SERVER_PORT') ? process.env['DUMMY_SERVER_PORT'] : 8080;
let server = new DummyServer(port);
server.initialize();
server.start();