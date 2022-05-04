const express = require('express');
const Logger = require('./system/logger.js');
const Express = require('./system/express.js');
const crypto = require('crypto');


class Router {

    static get METHODS() { return ['GET', 'POST', 'DELETE']; }

    static get_registry_key(method, path) {
        // hashes registry key based on method and path,
        // This is hashed because because the key/id will be used in url paths and cannot have slashes
        // regex removes trailing slashes (/) because express does not distinguish between slash and no slash
        // the registry should also not discriminate against slashes

        method = method.toUpperCase();
        path = Router.sanitize_path(path);
        return crypto.createHash('sha256').update(`${method}-${path}`).digest('hex');
    }

    constructor() {

        this.__log = new Logger();
        this.__router = null;
        this.__set = [];
        this.__descriptions = {}
    }

    initialize(server_factory=null) {
        if (server_factory === null)
            server_factory = new Express();
        this.__router = server_factory.create_router();
    }

    static sanitize_path(path) {
        let stripped = path.replace(/\/$/, "");
        if (stripped.length === 0)
            stripped = '/';
        return stripped
    }

    register(method, path, onCall, overrideable=false, description=null) {

        this.__descriptions[Router.get_registry_key(method, path)] = description;

        path = Router.sanitize_path(path);

        if (!overrideable) {
            let identifier = Router.get_registry_key(method, path);
            if (this.__set.includes(identifier)){
                return;
            }
            this.__set.push(identifier)
        }

        this.__log.write(`REGISTERED [${method}] ${path}`);
        switch (method) {
            case 'GET':
                this.__router.get(path, (request, response) => {
                    this.__log.write(`[${method}] ${path}`);
                    onCall(request, response)
                });
                return;
            case 'POST':
                this.__router.post(path, (request, response) => {
                    this.__log.write(`[${method}] ${path}`);
                    onCall(request, response)
                });
                return;
            case 'DELETE':
                this.__router.delete(path, (request, response) => {
                    this.__log.write(`[${method}] ${path}`);
                    onCall(request, response)
                });
                return;
        }
    }

    unregister(method, path) {
        let identifier = Router.get_registry_key(method, path);
        if (this.__set.includes(identifier))
            return;

        this.__log.write(`UNREGISTERED [${method}] ${path}`);
        // removes route from router stack
        this.__router.stack = this.__router.stack.filter(node => {
            let route = node.route;
            let node_method = route.stack.map(s => s['method'])[0].toUpperCase();
            return node_method !== method || route.path !== path;
        });
    }

    get stack() {
        // return this.__router.stack;
        let routes_description = this.__router.stack.map(routes => {

            return routes['route']['stack'].map(stack => {
                let path = routes['route']['path'];
                let registry_key = Router.get_registry_key(stack['method'], path);

                return {
                    path: path,
                    method: stack['method'],
                    overrideable: !this.__set.includes(registry_key),
                    registry_key: registry_key,
                    description: (this.__descriptions.hasOwnProperty(registry_key) && this.__descriptions[registry_key]) ? this.__descriptions[registry_key] : '',
                }
            });
        });

        //flattening array
        return [].concat.apply([], routes_description);
    }

    get router() {
        return this.__router
    }
} module.exports = Router;
