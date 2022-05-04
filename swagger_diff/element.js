const StringBuilder = require('./stringbuilder.js');
const Util = require('util');


class Element {

    constructor(name) {
        this.__name = name;
        this.__attributes = {};
        this.__content = [];
    }

    attributes(attributes) {
        Object.assign(this.__attributes, attributes);
    }

    content(content) {
        this.__content.push(content);
    }

    nest(elementBuilder) {
        this.content(elementBuilder);
    }

    toString() {
        let attributes = new StringBuilder();
        Object.keys(this.__attributes).forEach(key => {
            attributes.add(Util.format("%s=%s", key, this.__attributes[key]));
        });

        let builder = new StringBuilder();
        builder.addline(Util.format("<%s %s>", this.__name, attributes.toString()));

        this.__content.forEach(content => {
            builder.addline(content.toString());
        });

        builder.addline(Util.format("</%s>", this.__name));

        return builder.toString();
    }
}

module.exports = Element;