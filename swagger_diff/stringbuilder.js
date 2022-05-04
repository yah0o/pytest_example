const Util = require('util');


class StringBuilder {

    constructor() {
        this.__string = '';
    }

    add(string) {
        this.__string = Util.format('%s%s', this.__string, string);
    }

    addline(string) {
        this.__string = Util.format('%s%s\n', this.__string, string);
    }

    toString() {
        return this.__string;
    }
}

module.exports = StringBuilder;