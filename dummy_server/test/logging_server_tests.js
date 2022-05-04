const assert = require('assert');
const expect = require('expect.js');
const LoggingServer = require('../logging_server.js');
const Mocks = require('./mocks.js');


describe('Logging Server', () => {

    describe('\'/\'', () => {
        it('should respond with all files in the log directory', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);
            let mockFileSystem = new Mocks.MockFileSystem();
            mockFileSystem.files = {
                'test-1.log': {
                    content: 'test\ntest',
                    error: null
                },
                'test-2.log': {
                    content: 'test\ntest',
                    error: null
                },
            };

            let dummy_server = new LoggingServer(0, mockServerFactory);
            dummy_server.__log = new Mocks.MockLogger();
            dummy_server.__router = mockRouter;
            dummy_server.__filesystem = mockFileSystem;

            dummy_server.__data_registry = {
                not_test: true
            };

            dummy_server.initialize();
            let call = mockRouter.registered.find((reg) => (reg.method === 'GET' && reg.path === '/'));

            let mockRequest = new Mocks.MockRequest();
            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            expect(mockResponse.object).to.be.an('object');
            expect(mockResponse.object).to.only.have.keys(['error', 'files']);

            expect(mockResponse.object.error).to.be(null);

            expect(mockResponse.object.files.length).to.be(Object.keys(mockFileSystem.files).length);
            expect(mockResponse.object.files.map(f => f.filename)).to.eql(Object.keys(mockFileSystem.files));
            expect(mockResponse.object.files.map(f => f.error)).to.eql([null, null]);
            expect(mockResponse.object.files.map(f => f.logs)).to.eql(
                Object.values(mockFileSystem.files).map(f => f.content).map(content => content.split('\n'))
            );
        });

        it('should respond with error if directory errors', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);
            let mockFileSystem = new Mocks.MockFileSystem();
            mockFileSystem.err = 'directory_error';
            mockFileSystem.files = {
                'test-1.log': {
                    content: 'test\ntest',
                    error: null
                },
                'test-2.log': {
                    content: 'test\ntest',
                    error: null
                },
            };

            let dummy_server = new LoggingServer(0, mockServerFactory);
            dummy_server.__log = new Mocks.MockLogger();
            dummy_server.__router = mockRouter;
            dummy_server.__filesystem = mockFileSystem;

            dummy_server.__data_registry = {
                not_test: true
            };

            dummy_server.initialize();
            let call = mockRouter.registered.find((reg) => (reg.method === 'GET' && reg.path === '/'));

            let mockRequest = new Mocks.MockRequest();
            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            expect(mockResponse.object).to.only.have.keys(['error', 'files']);
            expect(mockResponse.object.error).to.be('directory_error');
        });

        it('should respond with error if file errors', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);
            let mockFileSystem = new Mocks.MockFileSystem();
            mockFileSystem.files = {
                'test-1.log': {
                    content: 'test\ntest',
                    error: 'file_error'
                },
                'test-2.log': {
                    content: 'test\ntest',
                    error: null
                },
            };

            let dummy_server = new LoggingServer(0, mockServerFactory);
            dummy_server.__log = new Mocks.MockLogger();
            dummy_server.__router = mockRouter;
            dummy_server.__filesystem = mockFileSystem;

            dummy_server.__data_registry = {
                not_test: true
            };

            dummy_server.initialize();
            let call = mockRouter.registered.find((reg) => (reg.method === 'GET' && reg.path === '/'));

            let mockRequest = new Mocks.MockRequest();
            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            expect(mockResponse.object).to.only.have.keys(['error', 'files']);
            expect(mockResponse.object.error).to.be(null);

            expect(mockResponse.object.files.length).to.be(Object.keys(mockFileSystem.files).length);
            expect(mockResponse.object.files.map(f => f.filename)).to.eql(Object.keys(mockFileSystem.files));
            expect(mockResponse.object.files.map(f => f.error)).to.eql(['file_error', null]);
            expect(mockResponse.object.files.map(f => f.logs)).to.eql(
                [null, ['test', 'test']]
            );
        });
    });

    describe('\'/files\'', () => {
        it('should respond with all files in the log directory', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);
            let mockFileSystem = new Mocks.MockFileSystem();
            mockFileSystem.files = {
                'test-1.log': {},
                'test-2.log': {},
            };

            let dummy_server = new LoggingServer(0, mockServerFactory);
            dummy_server.__log = new Mocks.MockLogger();
            dummy_server.__router = mockRouter;
            dummy_server.__filesystem = mockFileSystem;

            dummy_server.__data_registry = {
                not_test: true
            };

            dummy_server.initialize();
            let call = mockRouter.registered.find((reg) => (reg.method === 'GET' && reg.path === '/files'));

            let mockRequest = new Mocks.MockRequest();
            let mockResponse = new Mocks.MockResponse();
            call.onCall(mockRequest, mockResponse);

            expect(mockResponse.object).to.be.an('object');
            expect(mockResponse.object).to.only.have.keys(['error', 'files']);

            expect(mockResponse.object.error).to.be(null);

            expect(mockResponse.object.files.length).to.be(Object.keys(mockFileSystem.files).length);
            expect(mockResponse.object.files).to.eql(Object.keys(mockFileSystem.files));
            expect(mockResponse.object.error).to.eql(null);
        });
    });

    describe('\'/content/:filename\'', () => {
        it('should respond with content of specified log directory', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);
            let mockFileSystem = new Mocks.MockFileSystem();
            mockFileSystem.files = {
                'test-1.log': {
                    content: 'test\ntest',
                    error: null
                },
                'test-2.log': {
                    content: 'test\ntest',
                    error: null
                },
            };

            let dummy_server = new LoggingServer(0, mockServerFactory);
            dummy_server.__log = new Mocks.MockLogger();
            dummy_server.__router = mockRouter;
            dummy_server.__filesystem = mockFileSystem;
            dummy_server.__data_registry = {
                not_test: true
            };

            mockFileSystem.dirname = `${dummy_server.dirname}/logs`;

            dummy_server.initialize();
            let call = mockRouter.registered.find((reg) => (reg.method === 'GET' && reg.path === '/content/:filename'));

            let mockRequest = new Mocks.MockRequest();
            mockRequest.params = {filename: 'test-1.log'};
            let mockResponse = new Mocks.MockResponse();

            call.onCall(mockRequest, mockResponse);

            expect(mockResponse.object).to.be.an('object');
            expect(mockResponse.object).to.only.have.keys(['error', 'logs', 'lines']);

            expect(mockResponse.object.error).to.be(null);

            expect(mockResponse.object.logs.length).to.be(Object.keys(mockFileSystem.files).length);
            expect(mockResponse.object.error).to.eql(null);
        });
    });

    describe('#start()', () => {
        it('should start server listening', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);
            let port = 1234;

            let dummy_server = new LoggingServer(port, mockServerFactory);
            dummy_server.__log = new Mocks.MockLogger();
            dummy_server.__router = mockRouter;
            dummy_server.__filesystem = new Mocks.MockFileSystem();

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

            let dummy_server = new LoggingServer(0, mockServerFactory);
            dummy_server.__log = new Mocks.MockLogger();
            dummy_server.__router = mockRouter;
            dummy_server.__filesystem = new Mocks.MockFileSystem();

            dummy_server.initialize();
            expect(mockServer.router).not.be(null);
            expect(mockServer.use_count).be(1);
        });

        it('should register GET \'/\'', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new LoggingServer(0, mockServerFactory);
            dummy_server.__log = new Mocks.MockLogger();
            dummy_server.__router = mockRouter;
            dummy_server.__filesystem = new Mocks.MockFileSystem();

            dummy_server.initialize();
            let filtered = mockRouter.registered.filter((reg) => (reg.method === 'GET' && reg.path === '/'));
            expect(filtered.length).be(1);
        });

        it('should register GET \'/files\'', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new LoggingServer(0, mockServerFactory);
            dummy_server.__log = new Mocks.MockLogger();
            dummy_server.__router = mockRouter;
            dummy_server.__filesystem = new Mocks.MockFileSystem();

            dummy_server.initialize();
            let filtered = mockRouter.registered.filter((reg) => (reg.method === 'GET' && reg.path === '/files'));
            expect(filtered.length).be(1);
        });

        it('should register GET \'/content/:filename\'', () => {
            let mockRouter = new Mocks.MockRouter();
            let mockServer = new Mocks.MockServer();
            let mockServerFactory = new Mocks.MockExpress(mockServer);

            let dummy_server = new LoggingServer(0, mockServerFactory);
            dummy_server.__log = new Mocks.MockLogger();
            dummy_server.__router = mockRouter;
            dummy_server.__filesystem = new Mocks.MockFileSystem();

            dummy_server.initialize();
            let filtered = mockRouter.registered.filter((reg) => (reg.method === 'GET' && reg.path === '/content/:filename'));
            expect(filtered.length).be(1);
        });
    });
});