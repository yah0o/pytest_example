const Element = require('./element.js');
const Util = require('util');


class HTMLPageBuilder {

    constructor() {
        this.__page = new Element('html');
        this.__style = new Element('style');
        this.__page.nest(this.__style);
    }

    stylize(className, style) {
        this.__style.content(Util.format('%s %s', className, style));
    }

    nest(element) {
        this.__page.nest(element);
    }

    toString() {
        return this.__page.toString();
    }
}

module.exports = HTMLPageBuilder;