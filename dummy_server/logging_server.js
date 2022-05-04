const FileSystem = require('fs');
const Logger = require('./system/logger.js');
const Router = require('./router.js');
const Express = require('./system/express.js');


class LoggingServer {

    constructor(port, server_factory=null) {
        if (server_factory === null)
            server_factory = new Express();

        this.__filesystem = FileSystem; //for mocking out in UTs
        this.__log = new Logger();
        this.__port = port;
        this.__router = new Router();
        this.__server = server_factory.create_server();
    }

    get dirname() {
        return __dirname; //for unit tests
    }

    initialize() {
        this.__router.initialize();

        this.__router.register(
            'GET',
            '/',
            (request, response) => {
                let response_data = {
                    error: null,
                    files: [],
                };
                let log_dirname = `${this.dirname}/logs`;
                this.__filesystem.readdir(log_dirname, (err, filenames) => {
                    if (err) {
                        response_data.error = err;
                        return response.status(404).json(response_data);
                    }
                    filenames.forEach((filename) => {
                        this.__filesystem.readFile(`${log_dirname}/${filename}`, 'utf-8', (err, content) => {
                            let file_data = {
                                error: null,
                                logs: null,
                                lines: null,
                                filename: filename,
                            };
                            response_data.files.push(file_data);

                            if (err) {
                                file_data.error = err;
                                return;
                            }

                            let lines = content.split('\n');
                            file_data.logs = lines;
                            file_data.lines = lines.length;

                            if(response_data.files.length === filenames.length)
                                response.json(response_data)
                        });
                    });
                });
            }
        );

        this.__router.register('GET', '/content/:filename', (request, response) => {
            let filename = request.params.filename;

            let response_data = {
                error: null,
                logs: [],
                lines: null,
            };

            this.__filesystem.readFile(`${this.dirname}/logs/${filename}`, 'utf-8', (err, content) => {
                if (err) {
                    response_data.error = err;
                    return;
                }

                let lines = content.split('\n');
                if (lines.length > 1000)
                    lines = lines.slice(lines.length - 1000, lines.length);

                response_data.logs = lines;
                response_data.lines = lines.length;
                response.json(response_data)
            });
        });

        this.__router.register('GET', '/files', (request, response) => {
            let response_data = {
                error: null,
                files: [],
            };

            this.__filesystem.readdir(`${this.dirname}/logs`, (err, filenames) => {
                if (err) {
                    response_data.error = err;
                    return response.status(404).json(response_data);
                }
                response_data.files = filenames;
                return response.json(response_data);
            });
        });

        this.__server.use(this.__router.router);
    }

    start() {
        this.__server.listen(this.__port, '0.0.0.0', () => this.__log.write(`Dummy Server listening on port ${this.__port}`));
    }

} module.exports = LoggingServer;
