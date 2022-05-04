const assert = require('assert');
const expect = require('expect.js');
const Router = require('../router.js');
const Mocks = require('./mocks.js');


describe('Router', () => {

    describe('#initialize', () => {
        it('create new express router', () => {
            let router = new Router();
            router.__log = new Mocks.MockLogger();

            let mockExpressRouter = new Mocks.MockExpressRouter();
            let mockExpress = new Mocks.MockExpress();
            mockExpress.mock_router = mockExpressRouter;

            expect(mockExpress.created_router).to.be(false);
            router.initialize(mockExpress);
            expect(mockExpress.created_router).to.be(true);
        });
    });

    describe('#register', () => {
        it('should register get calls', () => {
            let mockExpressRouter = new Mocks.MockExpressRouter();

            let router = new Router();
            router.__router = mockExpressRouter;
            router.__log = new Mocks.MockLogger();

            let call_this = false;
            router.register('GET', '/test_path', () => {
                call_this = true;
            }, false);

            expect(router.__set.length).to.be(1);
            expect(mockExpressRouter.method).to.be('get');
            expect(mockExpressRouter.path).to.be('/test_path');

            mockExpressRouter.onCall({}, {});
            expect(call_this).to.be(true);
        });

        it('should register post calls', () => {
            let mockExpressRouter = new Mocks.MockExpressRouter();

            let router = new Router();
            router.__router = mockExpressRouter;
            router.__log = new Mocks.MockLogger();

            let call_this = false;
            router.register('POST', '/test_path', () => {
                call_this = true;
            }, false);

            expect(router.__set.length).to.be(1);
            expect(mockExpressRouter.method).to.be('post');
            expect(mockExpressRouter.path).to.be('/test_path');

            mockExpressRouter.onCall({}, {});
            expect(call_this).to.be(true);
        });

        it('should register post calls', () => {
            let mockExpressRouter = new Mocks.MockExpressRouter();

            let router = new Router();
            router.__router = mockExpressRouter;
            router.__log = new Mocks.MockLogger();

            let call_this = false;
            router.register('DELETE', '/test_path', () => {
                call_this = true;
            }, false);

            expect(router.__set.length).to.be(1);
            expect(mockExpressRouter.method).to.be('delete');
            expect(mockExpressRouter.path).to.be('/test_path');

            mockExpressRouter.onCall({}, {});
            expect(call_this).to.be(true);
        });

        it('should not override calls that are not overridable', () => {
            let mockExpressRouter = new Mocks.MockExpressRouter();

            let router = new Router();
            router.__router = mockExpressRouter;
            router.__log = new Mocks.MockLogger();

            router.register('DELETE', '/test_path', () => {}, false);

            expect(router.__set.length).to.be(1);
            expect(mockExpressRouter.register_count).to.be(1);
            expect(mockExpressRouter.method).to.be('delete');
            expect(mockExpressRouter.path).to.be('/test_path');

            router.register('DELETE', '/test_path', () => {}, false);
            expect(router.__set.length).to.be(1);
            expect(mockExpressRouter.register_count).to.be(1);
        });

        it('should override register calls that are overridable', () => {
            let mockExpressRouter = new Mocks.MockExpressRouter();

            let router = new Router();
            router.__router = mockExpressRouter;
            router.__log = new Mocks.MockLogger();

            router.register('DELETE', '/test_path', () => {}, true);

            expect(router.__set.length).to.be(0);
            expect(mockExpressRouter.register_count).to.be(1);
            expect(mockExpressRouter.method).to.be('delete');
            expect(mockExpressRouter.path).to.be('/test_path');

            router.register('DELETE', '/test_path', () => {}, true);
            expect(router.__set.length).to.be(0);
            expect(mockExpressRouter.register_count).to.be(2);
        });
    });

    describe('#unregister', () => {
        it('should not unregister non-overridable calls', () => {
            let mockExpressRouter = new Mocks.MockExpressRouter();

            let router = new Router();
            router.__router = mockExpressRouter;
            router.__log = new Mocks.MockLogger();
            router.__set.push(Router.get_registry_key('DELETE', '/test_path'));
            mockExpressRouter.stack = [{
                route: {
                    path: '/test_path',
                    stack: [{
                        method: 'DELETE'
                    }]
                }
            }];

            router.unregister('DELETE', '/test_path');
            expect(mockExpressRouter.stack.length).to.be(1);
        });

        it('should unregister noverridable calls', () => {
            let mockExpressRouter = new Mocks.MockExpressRouter();

            let router = new Router();
            router.__router = mockExpressRouter;
            router.__log = new Mocks.MockLogger();
            router.__set.push(`GET/test_path`);
            mockExpressRouter.stack = [{
                route: {
                    path: '/test_path',
                    stack: [{
                        method: 'DELETE'
                    }]
                }
            }];

            router.unregister('DELETE', '/test_path');
            expect(mockExpressRouter.stack.length).to.be(0);
        });
    });

    describe('#stack', () => {
        it('should return a json object per path per method', () => {
            let mockExpressRouter = new Mocks.MockExpressRouter();
            let stack = [{
                route: {
                    path: '/test_path',
                    stack: [{
                        method: 'DELETE'
                    }, {
                        method: 'GET'
                    }]
                }
            }];

            let router = new Router();
            router.__router = mockExpressRouter;
            router.__log = new Mocks.MockLogger();
            router.__set.push(Router.get_registry_key('DELETE', '/test_path'));
            mockExpressRouter.stack = stack;

            expect(router.stack).to.be.eql([{
                "description": "",
                "method": "DELETE",
                "overrideable": false,
                "path": "/test_path",
                "registry_key": Router.get_registry_key('DELETE', '/test_path'),
            }, {
                "description": "",
                "method": "GET",
                "overrideable": true,
                "path": "/test_path",
                "registry_key": Router.get_registry_key('GET', '/test_path'),
            }]);
        });
    });
});