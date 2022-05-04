const assert = require('assert');
const expect = require('expect.js');
const DummyServer = require('../dummy_server.js');
const Router = require('../router.js');
const Mocks = require('./mocks.js');


describe('Dummy Server', () => {

    describe('\'/readme\'', () => {
        it('should respond with file', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();
            let call = mockRouter.registered.find((reg) => (reg.method === 'GET' && reg.path === '/readme'));
            expect(call).not.be(undefined);

            let mockRequest = new Mocks.MockRequest();
            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            expect(mockResponse.file).not.be(null);
        });
    });

    describe('\'\/\'', () => {
        it('should respond with array of routes information', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();
            let call = mockRouter.registered.find((reg) => (reg.method === 'GET' && reg.path === '/'));

            let mockRequest = new Mocks.MockRequest();
            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            expect(mockResponse.object).to.be.an('array');
            expect(mockResponse.object.length).to.be(7);
        });
    });

    describe('\'/registry\'', () => {
        it('should respond with registry object', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server._data_registry = {
                not_test: true
            };

            dummy_server.initialize();
            let call = mockRouter.registered.find((reg) => (reg.method === 'GET' && reg.path === '/registry'));

            let mockRequest = new Mocks.MockRequest();
            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            expect(mockResponse.object).to.be.an('object');
            expect(mockResponse.object).to.only.have.keys(['not_test']);
            expect(mockResponse.object.not_test).to.be(true);
        });
    });

    describe('\'/logs/:registry_key\'', () => {
        it('should respond with logs associated with the specific key', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server._data_registry = {
                test: {
                    method: 'test',
                    path: '/test',
                    log: [1, 2, 3]
                }
            };

            dummy_server.initialize();

            let found = mockRouter.registered.find((reg) => (reg.method === 'GET' && reg.path === '/logs/:registry_key'));

            let mockRequest = new Mocks.MockRequest();
            mockRequest.params = {
                registry_key: 'test'
            };
            let mockResponse = new Mocks.MockResponse();
            found.onCall(mockRequest, mockResponse);

            expect(mockResponse.object).to.only.have.keys(['logs', 'path', 'error']);
            expect(mockResponse.object.error).to.be(null);
            expect(mockResponse.object.logs).to.be.an('array');
            expect(mockResponse.object.logs.length).to.be(3);
        });

        it('should return status 400 if requested key is not registered', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server._data_registry = {
                not_test: {
                    method: 'test',
                    path: '/test',
                    log: [1, 2, 3]
                }
            };

            dummy_server.initialize();

            let found = mockRouter.registered.find((reg) => (reg.method === 'GET' && reg.path === '/logs/:registry_key'));

            let mockRequest = new Mocks.MockRequest();
            mockRequest.params = {
                registry_key: 'test'
            };
            let mockResponse = new Mocks.MockResponse();
            found.onCall(mockRequest, mockResponse);

            expect(mockResponse.status_code).to.be(400);
            expect(mockResponse.object).to.only.have.keys(['logs', 'path', 'error']);
            expect(mockResponse.object.error).to.be('Cannot fetch logs for test because it has not been registered');
            expect(mockResponse.object.logs).to.be.an('array');
            expect(mockResponse.object.logs.length).to.be(0);
        });
    });

    describe('\'/unregister\'', () => {
        it('should unregister endpoint', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            let registry_key = Router.get_registry_key('GET', '/test');
            dummy_server._data_registry[registry_key] = {
                method: 'test',
                path: '/test',
                log: [1, 2, 3]
            };

            dummy_server.initialize();

            let found = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/unregister'));

            let mockRequest = new Mocks.MockRequest();
            mockRequest.body = {
                method: 'GET',
                path: '/test'
            };
            let mockResponse = new Mocks.MockResponse();
            found.onCall(mockRequest, mockResponse);

            expect(mockResponse.object).to.be.an('object');
            expect(mockResponse.object).to.only.have.keys(['success', 'error']);
            expect(mockResponse.object.success).to.be(true);
            expect(mockResponse.object.error).to.be(null);

            expect(dummy_server._data_registry).to.be.empty();

            expect(mockRouter.unregistered_path).be('/test');
            expect(mockRouter.unregistered_method).be('GET');

            expect(mockServer.use_count).be(2);
        });

        it('should return status 400 if request is missing method', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();
            let call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/unregister'));

            let mockRequest = new Mocks.MockRequest();
            mockRequest.body = {
                method: 'GET',
            };
            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            expect(mockResponse.object).to.be.an('object');
            expect(mockResponse.object).to.only.have.keys(['success', 'error']);
            expect(mockResponse.object.success).to.be(false);
            expect(mockResponse.object.error).to.be('Missing key method or path key');

            expect(mockRouter.unregistered_path).be(null);
            expect(mockRouter.unregistered_method).be(null);

            expect(mockServer.use_count).be(1);
        });

        it('should return status 400 if request is missing path', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();
            let call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/unregister'));

            let mockRequest = new Mocks.MockRequest();
            mockRequest.body = {
                path: '/test'
            };
            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            expect(mockResponse.object).to.be.an('object');
            expect(mockResponse.object).to.only.have.keys(['success', 'error']);
            expect(mockResponse.object.success).to.be(false);
            expect(mockResponse.object.error).to.be('Missing key method or path key');

            expect(mockRouter.unregistered_path).be(null);
            expect(mockRouter.unregistered_method).be(null);

            expect(mockServer.use_count).be(1);
        });

        it('should return status 400 if request is path does not start with /', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();
            let call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/unregister'));

            let mockRequest = new Mocks.MockRequest();
            mockRequest.body = {
                method: 'get',
                path: 'test'
            };
            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            expect(mockResponse.object).to.be.an('object');
            expect(mockResponse.object).to.only.have.keys(['success', 'error']);
            expect(mockResponse.object.success).to.be(false);
            expect(mockResponse.object.error).to.be('Path must start with /');

            expect(mockRouter.unregistered_path).be(null);
            expect(mockRouter.unregistered_method).be(null);

            expect(mockServer.use_count).be(1);
        });

        it('should return status 400 if requested endpoint is not registered', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            let registry_key = Router.get_registry_key('GET', '/test');
            dummy_server._data_registry[registry_key] = {
                method: 'test',
                path: '/test',
                log: [1, 2, 3]
            };

            dummy_server.initialize();
            let call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/unregister'));

            let mockRequest = new Mocks.MockRequest();
            mockRequest.body = {
                method: 'GET',
                path: '/not_test'
            };
            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            expect(mockResponse.status_code).to.be(400);
        });
    });

    describe('\'/(registered calls)\'', () => {
        it('should respond with registered content when called', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();
            let register_call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/register'));

            let register_mockRequest = new Mocks.MockRequest();
            register_mockRequest.body = {
                method: 'GET',
                path: '/a_test',
                content: {
                    'test': 'content'
                }
            };
            let register_mockResponse = new Mocks.MockResponse();
            register_call.onCall(register_mockRequest, register_mockResponse);

            let route = mockRouter.registered.find((reg) => (reg.method === 'GET' && reg.path === '/a_test'));
            let mockRequest = new Mocks.MockRequest();
            let mockResponse = new Mocks.MockResponse();
            route.onCall(mockRequest, mockResponse);
            expect(mockResponse.object).to.eql({ 'test': 'content' });
        });

        it('should respond with registered file when called', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();
            let register_call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/register'));

            let register_mockRequest = new Mocks.MockRequest();
            register_mockRequest.body = {
                method: 'GET',
                path: '/a_test',
                content: {
                    'test': 'content'
                }
            };
            let register_mockResponse = new Mocks.MockResponse();
            register_call.onCall(register_mockRequest, register_mockResponse);

            let attach_call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/attach/:registry_key'));
            let attach_call_mockRequest = new Mocks.MockRequest();
            attach_call_mockRequest.params = {
                registry_key: register_mockResponse.object.registry_key
            };
            attach_call_mockRequest.files = {
                file: new Mocks.MockFile('test.test')
            };
            let attach_call_mockResponse = new Mocks.MockResponse();
            attach_call.onCall(attach_call_mockRequest, attach_call_mockResponse);

            let route = mockRouter.registered.find((reg) => (reg.method === 'GET' && reg.path === '/a_test'));
            let mockRequest = new Mocks.MockRequest();
            let mockResponse = new Mocks.MockResponse();
            route.onCall(mockRequest, mockResponse);

            expect(mockResponse.object).to.eql(null);
            expect(mockResponse.file).to.be(`${DummyServer._this_directory}/files/test.test`);
        });

        it('should respond with registered status code when called', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();

            let register_call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/register'));
            let register_mockRequest = new Mocks.MockRequest();
            register_mockRequest.body = {
                method: 'GET',
                path: '/a_test',
                status_code: 1234
            };
            let register_mockResponse = new Mocks.MockResponse();
            register_call.onCall(register_mockRequest, register_mockResponse);

            let route = mockRouter.registered.find((reg) => (reg.method === 'GET' && reg.path === '/a_test'));
            let mockRequest = new Mocks.MockRequest();
            let mockResponse = new Mocks.MockResponse();
            route.onCall(mockRequest, mockResponse);
            expect(mockResponse.status_code).to.be(1234);
        });

        it('should respond with registered headers code when called', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();

            let register_call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/register'));
            let register_mockRequest = new Mocks.MockRequest();
            register_mockRequest.body = {
                method: 'GET',
                path: '/a_test',
                headers: {
                    'test': 'headers'
                }
            };
            let register_mockResponse = new Mocks.MockResponse();
            register_call.onCall(register_mockRequest, register_mockResponse);

            let route = mockRouter.registered.find((reg) => (reg.method === 'GET' && reg.path === '/a_test'));
            let mockRequest = new Mocks.MockRequest();
            let mockResponse = new Mocks.MockResponse();
            route.onCall(mockRequest, mockResponse);
            expect(mockResponse.headers).to.eql({ 'test': 'headers' });
        });

        it('should write to log when called', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();

            let register_call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/register'));
            let register_mockRequest = new Mocks.MockRequest();
            register_mockRequest.body = {
                method: 'GET',
                path: '/a_test',
                content: {
                    'test': 'response'
                }
            };
            let register_mockResponse = new Mocks.MockResponse();
            register_call.onCall(register_mockRequest, register_mockResponse);

            let registered = dummy_server._data_registry[register_mockResponse.object['registry_key']];
            expect(registered.log.length).to.be(0);

            let route = mockRouter.registered.find((reg) => (reg.method === 'GET' && reg.path === '/a_test'));
            let mockRequest = new Mocks.MockRequest();
            mockRequest.body = {
                'test': 'request'
            };
            let mockResponse = new Mocks.MockResponse();
            route.onCall(mockRequest, mockResponse);

            expect(registered.log.length).to.be(1);
            let call_log = registered.log[0];
            expect(call_log).to.only.have.keys(['request', 'response', 'time', 'remote_address', 'id']);
            expect(call_log.request).to.eql({ 'test': 'request' });
            expect(call_log.response).to.eql({ 'test': 'response' });
        });

        it('should delete to log after 43200 seconds', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let mockTimer = new Mocks.MockTimer();

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = mockTimer;

            dummy_server.initialize();

            let register_call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/register'));
            let register_mockRequest = new Mocks.MockRequest();
            register_mockRequest.body = {
                method: 'GET',
                path: '/a_test',
            };
            let register_mockResponse = new Mocks.MockResponse();
            register_call.onCall(register_mockRequest, register_mockResponse);

            let registered = dummy_server._data_registry[register_mockResponse.object['registry_key']];
            expect(registered.log.length).to.be(0);

            let route = mockRouter.registered.find((reg) => (reg.method === 'GET' && reg.path === '/a_test'));
            let mockRequest = new Mocks.MockRequest();
            let mockResponse = new Mocks.MockResponse();
            route.onCall(mockRequest, mockResponse);

            expect(registered.log.length).to.be(1);
            expect(mockTimer.seconds).to.be(43200);

            mockTimer.func();

            expect(registered.log.length).to.be(0);
        });
    });

    describe('\'/register\'', () => {
        it('should add to the registry', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();

            let call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/register'));
            let mockRequest = new Mocks.MockRequest();
            mockRequest.body = {
                method: 'GET',
                path: '/not_test',
                headers: { 'test': 'test' },
                status_code: 1234,
                content: { 'content': 'test' }
            };

            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            let route = mockRouter.registered.filter((reg) => (reg.method === 'GET' && reg.path === '/not_test'));

            expect(route.length).to.be(1);
            expect(mockResponse.object).to.only.have.keys(['registry_key', 'error']);
            expect(mockResponse.object.error).to.be(null);

            let registered = dummy_server._data_registry[mockResponse.object['registry_key']];
            expect(registered).to.only.have.keys(['method', 'path', 'headers', 'status_code', 'content', 'log']);
            expect(registered.method).to.be('GET');
            expect(registered.path).to.be('/not_test');
            expect(registered.headers).to.eql({ 'test': 'test' });
            expect(registered.status_code).to.be(1234);
            expect(registered.content).to.eql({ 'content': 'test' });

        });

        it('should have headers, status code and content as optional', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();

            let call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/register'));
            let mockRequest = new Mocks.MockRequest();
            mockRequest.body = {
                method: 'GET',
                path: '/not_test',
            };
            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            let route = mockRouter.registered.filter((reg) => (reg.method === 'GET' && reg.path === '/not_test'));

            expect(route.length).to.be(1);
            expect(mockResponse.object).to.only.have.keys(['registry_key', 'error']);
            expect(mockResponse.object.error).to.be(null);

            let registered = dummy_server._data_registry[mockResponse.object['registry_key']];
            expect(registered).to.only.have.keys(['method', 'path', 'headers', 'status_code', 'content', 'log']);
            expect(registered.method).to.be('GET');
            expect(registered.path).to.be('/not_test');
            expect(registered.headers).to.eql({});
            expect(registered.status_code).to.be(200);
            expect(registered.content).to.eql({});
        });

        it('should respond with 400 if method is invalid', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();

            let call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/register'));
            let mockRequest = new Mocks.MockRequest();
            mockRequest.body = {
                method: 'INVALID',
                path: '/not_test',
            };
            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            expect(mockResponse.status_code).to.be(400);
            expect(mockResponse.object).to.only.have.keys(['registry_key', 'error']);
            expect(mockResponse.object.registry_key).to.be(null);
            expect(mockResponse.object.error).to.be('Method INVALID is not supported');
        });

        it('should return status 400 if request is missing method', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();
            let call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/register'));
            let mockRequest = new Mocks.MockRequest();
            mockRequest.body = {
                method: 'GET',
            };
            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            expect(mockResponse.object).to.be.an('object');
            expect(mockResponse.object).to.only.have.keys(['registry_key', 'error']);
            expect(mockResponse.object.registry_key).to.be(null);
            expect(mockResponse.object.error).to.be('Missing key method or path key');

            expect(mockRouter.unregistered_path).be(null);
            expect(mockRouter.unregistered_method).be(null);

            expect(mockServer.use_count).be(1);
        });

        it('should return status 400 if request is missing path', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();
            let call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/register'));
            let mockRequest = new Mocks.MockRequest();
            mockRequest.body = {
                path: '/test'
            };
            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            expect(mockResponse.object).to.be.an('object');
            expect(mockResponse.object).to.only.have.keys(['registry_key', 'error']);
            expect(mockResponse.object.registry_key).to.be(null);
            expect(mockResponse.object.error).to.be('Missing key method or path key');

            expect(mockRouter.unregistered_path).be(null);
            expect(mockRouter.unregistered_method).be(null);

            expect(mockServer.use_count).be(1);
        });

        it('should return status 400 if request is path does not start with /', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();
            let call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/register'));
            let mockRequest = new Mocks.MockRequest();
            mockRequest.body = {
                method: 'get',
                path: 'test'
            };
            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            expect(mockResponse.object).to.be.an('object');
            expect(mockResponse.object).to.only.have.keys(['registry_key', 'error']);
            expect(mockResponse.object.registry_key).to.be(null);
            expect(mockResponse.object.error).to.be('Path must start with /');

            expect(mockRouter.unregistered_path).be(null);
            expect(mockRouter.unregistered_method).be(null);

            expect(mockServer.use_count).be(1);
        });
    });

    describe('\'/attach/:registry_key\'', () => {
        it('should error 400 if registry key is not registered', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server._data_registry['test'] = {};

            dummy_server.initialize();

            let call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/attach/:registry_key'));
            let mockRequest = new Mocks.MockRequest();
            mockRequest.params = {
                registry_key: 'not_test'
            };
            mockRequest.files = {
                file: new Mocks.MockFile('test.test')
            };
            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            expect(mockResponse.status_code).to.be(400);
            expect(mockResponse.object).to.only.have.keys(['attached', 'error']);
            expect(mockResponse.object.attached).to.be(false);
            expect(mockResponse.object.error).to.be('Cannot attach file to not_test because it has not been registered');
        });

        it('should error 400 if no files are sent', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server._data_registry['test'] = {};

            dummy_server.initialize();

            let call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/attach/:registry_key'));
            let mockRequest = new Mocks.MockRequest();
            mockRequest.params = {
                registry_key: 'test'
            };
            mockRequest.files = null;
            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            expect(mockResponse.status_code).to.be(400);
            expect(mockResponse.object).to.only.have.keys(['attached', 'error']);
            expect(mockResponse.object.attached).to.be(false);
            expect(mockResponse.object.error).to.be('No files found in request. Cannot attach no files');
        });

        it('should attach files', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server._data_registry['test'] = {};

            dummy_server.initialize();

            let attach_call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/attach/:registry_key'));
            let mockRequest = new Mocks.MockRequest();
            mockRequest.params = {
                registry_key: 'test'
            };
            mockRequest.files = {
                file: new Mocks.MockFile('test.test')
            };
            let mockResponse = new Mocks.MockResponse();
            attach_call.onCall(mockRequest, mockResponse);

            expect(mockResponse.status_code).to.be(200);
            expect(mockResponse.object).to.only.have.keys(['attached', 'error']);
            expect(mockResponse.object.attached).to.be(true);
            expect(mockResponse.object.error).to.be(null);

            let registered = dummy_server._data_registry['test'];
            expect(registered.file).to.be(`${DummyServer._this_directory}/files/test.test`);
            expect(registered.file_name).to.be('test.test');
        });

        it('should respond with 500 error if there is a file error', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server._data_registry['test'] = {};

            dummy_server.initialize();
            let call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/attach/:registry_key'));
            let mockRequest = new Mocks.MockRequest();
            mockRequest.params = {
                registry_key: 'test'
            };
            mockRequest.files = {
                file: new Mocks.MockFile('test.test', 'file_error')
            };
            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            expect(mockResponse.status_code).to.be(500);
            expect(mockResponse.object).to.only.have.keys(['attached', 'error']);
            expect(mockResponse.object.attached).to.be(false);
            expect(mockResponse.object.error).to.be('file_error');
        });

        it('should respond with 500 error if there is a directory error', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem('directory error');
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server._data_registry['test'] = {};

            dummy_server.initialize();
            let call = mockRouter.registered.find((reg) => (reg.method === 'POST' && reg.path === '/attach/:registry_key'));
            let mockRequest = new Mocks.MockRequest();
            mockRequest.params = {
                registry_key: 'test'
            };
            mockRequest.files = {
                file: new Mocks.MockFile('test.test')
            };
            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            expect(mockResponse.status_code).to.be(500);
            expect(mockResponse.object).to.only.have.keys(['attached', 'error']);
            expect(mockResponse.object.attached).to.be(false);
            expect(mockResponse.object.error).to.be('directory error');
        });
    });

    describe('#start()', () => {
        it('should start server listening', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);
            let port = 1234;

            let dummy_server = new DummyServer(port, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.start();

            expect(mockServer.port).be(port);
            expect(mockServer.ip).be('0.0.0.0');
            expect(mockServer.callback).not.be(null);
        });
    });

    describe('#initialize()', () => {
        it('should register router', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();
            expect(mockServer.router).not.be(null);
            expect(mockServer.use_count).be(1);
        });

        it('should register GET \'/\'', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();
            let filtered = mockRouter.registered.filter((reg) => (reg.method === 'GET' && reg.path === '/'));
            expect(filtered.length).be(1);
        });

        it('should register GET \'/readme\'', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();
            let filtered = mockRouter.registered.filter((reg) => (reg.method === 'GET' && reg.path === '/readme'));
            expect(filtered.length).be(1);
        });

        it('should register GET \'/registry\'', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();
            let filtered = mockRouter.registered.filter((reg) => (reg.method === 'GET' && reg.path === '/registry'));
            expect(filtered.length).be(1);
        });

        it('should register GET \'/logs/:registry_key\'', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();
            let filtered = mockRouter.registered.filter((reg) => (reg.method === 'GET' && reg.path === '/logs/:registry_key'));
            expect(filtered.length).be(1);
        });

        it('should register POST \'/unregister\'', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();
            let filtered = mockRouter.registered.filter((reg) => (reg.method === 'POST' && reg.path === '/unregister'));
            expect(filtered.length).be(1);
        });

        it('should register POST \'/register\'', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();
            let filtered = mockRouter.registered.filter((reg) => (reg.method === 'POST' && reg.path === '/register'));
            expect(filtered.length).be(1);
        });

        it('should register POST \'/attach/:registry_key\'', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new DummyServer(0, mockServerFactory);
            dummy_server._log = new Mocks.MockLogger();
            dummy_server._router = mockRouter;
            dummy_server._filesystem = new Mocks.MockFileSystem();
            dummy_server._timer = new Mocks.MockTimer();

            dummy_server.initialize();
            let filtered = mockRouter.registered.filter((reg) => (reg.method === 'POST' && reg.path === '/attach/:registry_key'));
            expect(filtered.length).be(1);
        });
    });
});