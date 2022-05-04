const SwaggerGraphNode = require('./graphnode');


//for massaging data into usable ways.
class SwaggerGraph {

    constructor(json) {
        //swagger json separates paths and definitions into separate objects
        //this combines them into one bucket because for what we are using them for
        // they're kind of the same.
        let nodes = {};
        Object.keys(json.paths).forEach((path) => nodes[path] = json.paths[path]);
        Object.keys(json.definitions).forEach((definition) => nodes[definition] = json.definitions[definition]);

        //initializes nodes for graph
        this.__graph = {};
        Object.keys(nodes).forEach(node_name => {
            this.__graph[node_name] = new SwaggerGraphNode(node_name, nodes[node_name])
        });
        //this requires this.__graph to be completely finished filled out
        Object.keys(this.__graph).forEach(node_name => this.__graph[node_name].findSources(this.__graph));
    }

    get graph() {
        return this.__graph;
    }

    get nodes() {
        let nodes = [];
        Object.keys(this.__graph).forEach(path => nodes.push(this.__graph[path]));
        return nodes;
    }

    static merge(olderGraph, newerGraph) {

        newerGraph.nodes.forEach(node => {
            if (!olderGraph.hasNode(node.name))
                olderGraph.addNode(node);
            else
                olderGraph.getNode(node.name).combine(node);
        });
        return olderGraph;
    }

    hasNode(node_name) {
        return this.__graph.hasOwnProperty(node_name);
    }

    addNode(node) {
        this.__graph[node.name] = node;
    }

    getNode(node_name) {
        return this.__graph[node_name];
    }
}

module.exports = SwaggerGraph;