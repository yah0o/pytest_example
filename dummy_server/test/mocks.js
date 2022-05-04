
class MockExpress {
    constructor(mock_server) {
        this.mock_server = mock_server;
        this.mock_router = null;
        this.created_router = false;
    }

    create_server() {
        return this.mock_server;
    }

    create_router() {
        this.created_router = true;
        return this.mock_router;
    }
}


class MockExpressRouter {
    constructor() {
        this.stack = [];
        this.path = null;
        this.onCall = null;
        this.method = null;
        this.register_count = 0;
    }

    get(path, onCall) {
        this.register_count ++;
        this.method = 'get';
        this.path = path;
        this.onCall = onCall;
    }

    post(path, onCall) {
        this.register_count ++;
        this.method = 'post';
        this.path = path;
        this.onCall = onCall;
    }

    delete(path, onCall) {
        this.register_count ++;
        this.method = 'delete';
        this.path = path;
        this.onCall = onCall;
    }
}


class MockTimer {
    constructor () {
        this.func = null;
        this.seconds = null;
    }
    timeout(seconds, run){
        this.func = run
        this.seconds = seconds
    }
}


class MockFileSystem {
    constructor(err) {
        this.err = err;
        this.made = null;
        this.files = {}; //{ 'filename.txt': 'contents and stuff' }
        this.dirname = null;
        this.encoding = null;
    }
    mkdir(destination_folder, onFinish) {
        this.made = destination_folder;
        onFinish(this.err);
    }
    readdir(dirname, onFiles) {
        this.dirname = dirname;
        onFiles(this.err, Object.keys(this.files));
    }

    readFile(filename, encoding, onContents) {
        this.encoding = encoding;
        filename = filename.replace(`${this.dirname}/`, '');
        let contents = this.files[filename].content;
        let err = this.files[filename].error;
        onContents(err, contents);
    }
}


class MockFile {
    constructor(name, err) {
        this.err = err;
        this.name = name;
        this.move_to = null;
    }
    mv(file_location, onFinish) {
        this.move_to = file_location;
        onFinish(this.err)
    }
}


class MockServer {
    constructor() {
        this.router = null;
        this.port = null;
        this.ip = null;
        this.callback = null;
        this.use_count = 0
    }

    use(router) {
        this.use_count++;
        this.router = router;
    }

    listen(port, ip, callback) {
        this.port = port;
        this.ip = ip;
        this.callback = callback;
    }
}


class MockRouter {

    constructor() {
        this.__router = null;
        this.__set = [];
        this.registered = [];
        this.__stack = [];
        this.unregistered_path = null;
        this.unregistered_method = null;
    }

    initialize() {
    }

    register(method, path, onCall, overrideable=false) {
        this.registered.push({
            method: method,
            path: path,
            onCall: onCall,
            overrideable: overrideable
        });

        this.__stack.push({
            route: {
                path: path,
                stack: [{
                    method: method
                }]
            }
        })
    }

    unregister(method, path) {
        this.unregistered_path = path;
        this.unregistered_method = method;
    }

    get stack() {
        return this.__stack
    }

    get router() {
        return this.__stack
    }
}


class MockResponse {
    constructor() {
        this.object = null;
        this.file = null;
        this.status_code = 200;
        this.headers = {}
    }
    setHeader(key, value) {
        this.headers[key] = value;
    }
    json(object) {
        this.object = object
    }
    sendFile(file) {
        this.file = file;
    }
    status(status) {
        this.status_code = status;
        return this;
    }
}


class MockRequest {
    constructor() {
        this.params = {};
        this.body = {};
        this.files = null;
        this.connection = {remoteAddress: '123.4.5.6'};
    }
}


class MockLogger {
    constructor() {
        this.lines = []
    }
    write(line) {
        this.lines.push(line);
    }
}

module.exports = {
    MockExpress: MockExpress,
    MockExpressRouter: MockExpressRouter,
    MockTimer: MockTimer,
    MockFileSystem: MockFileSystem,
    MockFile: MockFile,
    MockServer: MockServer,
    MockRouter: MockRouter,
    MockResponse: MockResponse,
    MockRequest: MockRequest,
    MockLogger: MockLogger,
};