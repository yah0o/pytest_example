class SwaggerGraphNode {

    constructor(name, data) {

        this.__name = name;
        this.__references = this.__findAndCleanReferences(data);
        this.__referencedBy = [];
        this.__messages = [];
        this.__data = data;
        this.__methods = [];

        Object.keys(data).forEach(key => {
            if (SwaggerGraphNode.HTTP_METHODS.includes(key)) {
                this.__methods.push(key);
            }
        });

        this.__properties = null;
        if (data.hasOwnProperty('properties'))
            this.__properties = data.properties;
    }

    static get HTTP_METHODS() {
        return ['get', 'post', 'put', 'patch', 'delete'];
    }

    get methods() {
        return this.__methods;
    }

    get data() {
        return this.__data;
    }

    get name() {
        return this.__name;
    }

    get references() {
        return this.__references;
    }

    get referencedBy() {
        return this.__referencedBy;
    }

    get messages() {
        return this.__messages;
    }

    get properties() {
        return this.__properties;
    }

    get propertiesAndTypes() {
        let propertiesAndTypes = {};
        if (this.__properties !== null) {
            Object.keys(this.__properties).forEach(key => {

                propertiesAndTypes[key] = this.__properties[key].type;
                if (this.__properties[key].type === undefined)
                    propertiesAndTypes[key] = this.__properties[key].$ref;
            });
        }
        return propertiesAndTypes;
    }

    addMessage(message) {
        this.__messages.push(message);
    }

    combine(other_node) {
        this.__references = Array.from(new Set(this.references.concat(other_node.references)));
        this.__referencedBy = Array.from(new Set(this.referencedBy.concat(other_node.referencedBy)));
        this.__messages = Array.from(new Set(this.messages.concat(other_node.messages)));
        this.__properties = other_node.properties;
    }

    findSources(graph) {
        Object.keys(graph).forEach(other_node_name => {
            let other_node = graph[other_node_name];
            if (other_node.references.includes(this.__name))
                this.__referencedBy.push(other_node.name)
        });
    }

    __findAndCleanReferences(data) {

        let children = [];
        let objectsToSearch = [data];

        while (objectsToSearch.length > 0) {

            let object = objectsToSearch.pop();

            Object.keys(object).forEach(key => {
                if (typeof object[key] === 'object')
                    objectsToSearch.push(object[key]);
                if (key === '$ref')
                    children.push(object[key].replace('#/definitions/', ''));
            });
        }

        return children;
    }
}

module.exports = SwaggerGraphNode;
