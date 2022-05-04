const LoggingServer = require('./logging_server.js');


let port = process.env.hasOwnProperty('LOGGING_SERVER_PORT') ? process.env['LOGGING_SERVER_PORT'] : 9000;
let server = new LoggingServer(port);
server.initialize();
server.start();