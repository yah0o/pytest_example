const EventEmitter = require('events');
const Http = require('http');
const Https = require('https');


/**
 * get_data
 * a basic that allows ambiguity between http and https because those things are different in node.js
 */
class Request extends EventEmitter {

    static get ON_DATA() {
        return 'data';
    }

    static get ON_ERROR() {
        return 'error';
    }

    /**
     * get_data
     *
     * ex: request.get_data(Url.parse('https://api-wgie.wargaming.net/tools/swagger.json'));
     * @param {Url} url - html string to swagger json of an old version
     * @event Request#ON_DATA
     * @event Request#ON_ERROR
     */
    get_data(url) {
        let protocol = url.protocol;
        let options = {hostname: url.hostname, path: url.path};
        let data = '';

        if (protocol === 'https:')
            Https.get(options, response => {
                response.on('data', (chunk) => {
                    data += chunk;
                });
                response.on('end', () => {
                    this.emit(Request.ON_DATA, data);
                });
            }).on('error', (e) => {
                this.emit(Request.ON_ERROR, e);
            });

        else if (protocol === 'http:')
            Http.get(options, response => {
                response.on('data', (chunk) => {
                    data += chunk;
                });
                response.on('end', () => {
                    this.emit(Request.ON_DATA, data);
                });
            }).on('error', (e) => {
                this.emit(Request.ON_ERROR, e);
            });
    }
}

module.exports = Request;
