const crypto = require('crypto');
const FileSystem = require('fs');
const Logger = require('./system/logger.js');
const Router = require('./router.js');
const Express = require('./system/express.js');
const Timer = require('./system/timer.js');


class DummyServer {

    // (12hrs)
    static get LOG_TIMEOUT() { return 43200;}

    static create_random_id() {
        //creates dynamic id based on time and random
        let time = new Date().getTime().toString();
        let token = crypto.randomBytes(64).toString('hex');
        return crypto.createHash('sha256').update(`${time}${token}`).digest('hex');
    }

    constructor(port, server_factory=null) {
        if (server_factory === null)
            server_factory = new Express();

        this._data_registry = {};
        this._filesystem = FileSystem;
        this._log = new Logger();
        this._port = port;
        this._router = new Router();
        this._server = server_factory.create_server();
        this._timer = Timer;
    }

    initialize() {
        this._router.initialize();

        this._router.register(
            'GET',
            '/',
            (request, response) => {
                response.json(this._router.stack.map(routes => {
                    let data = this._data_registry.hasOwnProperty(routes.registry_key) ? this._data_registry[routes.registry_key] : null;

                    return {
                        description: routes.description,
                        path: routes.path,
                        dynamic_register: routes.overrideable,
                        registry_key: routes.registry_key,
                        method: routes.method,
                        will_respond_content: data ? data.content : null,
                        will_respond_headers: data ? data.headers : null,
                        will_respond_code: data ? data.status_code : null,
                    }
                }));
            },
            false,
            'Returns a list of registered routes and methods'
        );

        this._router.register(
            'GET',
            '/readme',
            (request, response) => response.sendFile(`${DummyServer._this_directory}/readme.html`),
            false,
            'Brings up documentation.'
        );

        this._router.register(
            'GET',
            '/registry',
            (request, response) => response.json(this._data_registry),
            false,
            'Returns all of the registered routes and the corresponding data'
        );

        this._router.register(
            'GET',
            '/logs/:registry_key',
            (request, response) => {
                let response_data = {
                    error: null,
                    path: null,
                    logs: [],
                };

                let registry_key = request.params.registry_key;
                if (!this._data_registry.hasOwnProperty(registry_key)) {
                    response_data.error = `Cannot fetch logs for ${registry_key} because it has not been registered`;
                    return response.status(400).json(response_data);
                }

                let registered = this._data_registry[registry_key];
                let method = registered.method;
                let path = registered.path;
                this._log.write(`GET logs for ${method}${path}`);

                response_data.logs = registered.log;
                response_data.path = registered.path;
                return response.json(response_data);
            },
            false,
            'Returns the logs for a certain call.'
        );

        this._router.register(
            'POST',
            '/unregister',
            (request, response) => {
                let response_data = {
                    error: null,
                    success: false,
                };

                if (!request.body.hasOwnProperty('method') || !request.body.hasOwnProperty('path')) {
                    response_data.error = `Missing key method or path key`;
                    return response.status(400).json(response_data);
                }

                if (!request.body.path.startsWith('/')) {
                    response_data.error = `Path must start with /`;
                    return response.status(400).json(response_data);
                }

                request.body.method = request.body.method.toUpperCase();

                let method = request.body.method;
                let path = request.body.path;

                let registry_key = Router.get_registry_key(method, path);
                if (!this._data_registry.hasOwnProperty(registry_key)) {
                    response_data.error = `Cannot unregister ${method} ${path} because it has not been registered`;
                    return response.status(400).json(response_data);
                }

                //re-registers router with server
                this._router.unregister(method, path);
                this._server.use(this._router.router);

                // removes data from registry
                delete this._data_registry[registry_key];

                response_data.success = true;
                return response.json(response_data);
            },
            false,
            'Unregisters a call.'
        );

        this._router.register(
            'POST',
            '/register',
            (request, response) => {
                let response_data = {
                    error: null,
                    registry_key: null,
                };

                if (!request.body.hasOwnProperty('method') || !request.body.hasOwnProperty('path')) {
                    response_data.error = `Missing key method or path key`;
                    return response.status(400).json(response_data);
                }

                if (!request.body.path.startsWith('/')) {
                    response_data.error = `Path must start with /`;
                    return response.status(400).json(response_data);
                }

                request.body.method = request.body.method.toUpperCase();

                let method = request.body.method;
                let path = request.body.path;
                let description = request.body.description ? request.body.description : '';
                let headers = request.body.hasOwnProperty('headers') && request.body['headers'] !== null ? request.body.headers : {};
                let status_code = request.body.hasOwnProperty('status_code') && request.body['status_code'] !== null ? request.body.status_code : 200;
                let content = request.body.hasOwnProperty('content') && request.body['content'] !== null ? request.body['content'] : {};

                if(!Router.METHODS.includes(method)) {
                    response_data.error = `Method ${method} is not supported`;
                    return response.status(400).json(response_data);
                }

                let registry_key = Router.get_registry_key(method, path);

                if (!this._data_registry.hasOwnProperty(registry_key))
                    this._router.register(method, path, (req, res) => this._get_value(method, path, req, res), true, description);

                this._data_registry[registry_key] = {
                    method: method,
                    path: path,
                    headers: headers,
                    status_code: status_code,
                    content: content,
                    log: [],
                };

                response_data.registry_key = registry_key;
                return response.json(response_data);
            },
            false,
            'Registers a call.'
        );

        this._router.register(
            'POST',
            '/attach/:registry_key',
            (request, response) => {
                let response_data = {
                    error: null,
                    attached: false,
                };

                let registry_key = request.params.registry_key;
                let files = request.files;

                if (!this._data_registry.hasOwnProperty(registry_key)) {
                    response_data.error = `Cannot attach file to ${registry_key} because it has not been registered`;
                    return response.status(400).json(response_data);
                }

                if (!(files && files.file)) {
                    response_data.error = 'No files found in request. Cannot attach no files';
                    return response.status(400).json(response_data);
                }

                let testFile = files.file;
                let destination_folder = `${DummyServer._this_directory}/files`;

                this._filesystem.mkdir(destination_folder, (dir_err) => {
                    if (dir_err && dir_err.code !== 'EEXIST') {
                        response_data.error = dir_err;
                        return response.status(500).json(response_data);
                    }

                    // Use the mv() method to place the file somewhere on server
                    let file_location = `${destination_folder}/${testFile.name}`;
                    testFile.mv(file_location, (file_err) => {
                        if (file_err) {
                            response_data.error = file_err;
                            return response.status(500).json(response_data);
                        }

                        let registry = this._data_registry[registry_key];
                        registry.file = file_location;
                        registry.file_name = testFile.name;

                        this._log.write(`Downloaded to ${file_location}`);
                        this._log.write(`Attached: ${testFile.name} to ${registry.method}${registry.path}`);

                        response_data.attached = true;
                        return response.json(response_data);
                    });
                });
            },
            false,
            'Attach a file that will be returned when the call is called.  Call must be registered before using this call'
        );

        this._server.use(this._router.router);
    }

    start() {
        this._server.listen(this._port, '0.0.0.0', () => this._log.write(`Dummy Server listening on port ${this._port}`));
    }

    static get _this_directory() {
        return __dirname;
    }

    _get_value(method, path, request, response) {

        let registry_key = Router.get_registry_key(method, path);

        let registered = this._data_registry[registry_key];

        let log_id = DummyServer.create_random_id();
        this._log.write(`requested ${method}${path} > log id: ${log_id}`);
        registered.log.push({
            request: request.body,
            response: registered.file ? 'FILE' : registered.content,
            time: new Date().toString(),
            id: log_id,
            remote_address: request.connection.remoteAddress
        });

        //will delete log after a period of time
        this._timer.timeout(DummyServer.LOG_TIMEOUT, () => {
            this._log.write(`TIMEOUT log ${log_id} for ${registry_key}`);
            if (!this._data_registry.hasOwnProperty(registry_key)) {
                this._log.write(`could not find ${registry_key}`);
                return;
            }

            this._data_registry[registry_key].log = this._data_registry[registry_key].log.filter(log => log.id !== log_id);
        });

        //add to response headers
        Object.keys(registered.headers).forEach(header => {
            response.setHeader(header, registered.headers[header]);
        });

        if (registered.file)
            return response.sendFile(`${registered.file}`);

        return response.status(registered.status_code).json(registered.content);
    }
} module.exports = DummyServer;
