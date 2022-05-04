const Gatherer = require('./gatherer.js');
const EventEmitter = require('events');
const Request = require('./request.js');
const SwaggerDiff = require('swagger-diff');
const SwaggerGraph = require('./graph.js');
const HTMLPageBuilder = require('./page.js');
const Url = require('url');
const Util = require('util');
const Element = require('./element.js');
const Filesystem = require('fs');


class Swagger extends EventEmitter {

    static get ON_GRAPH() {
        return 'graph';
    }

    static get ON_DIFF() {
        return 'swagger_diff';
    }

    static get ON_ERROR() {
        return 'error';
    }

    static get ON_WRITTEN() {
        return 'on_written';
    }

    static __createKeyName(message) {
        let key_name;

        if (message.path !== null)
            key_name = message.path;
        else if (message.descriptionPath !== null)
            key_name = message.descriptionPath;

        if (key_name === undefined)
            return key_name;

        key_name = key_name.replace('/paths/', '');
        key_name = key_name.replace('/definitions/', '');
        key_name = key_name.replace('definitions/', '');

        if (key_name.includes('/get/'))
            key_name = key_name.substring(0, key_name.indexOf('/get/'));
        if (key_name.includes('/properties/'))
            key_name = key_name.substring(0, key_name.indexOf('/properties/'));

        return key_name;
    }

    /**
     * makeGraph
     * creates a dependency graph for swagger objects with diff messages.
     * ex: swagger.makeGraph(
     *              'https://api-wgie.wargaming.net/tools/swagger.json',
     *              'https://api-wgie.wargaming.net/tools/swagger.json',
     *              ['edit-description', 'edit-summary']
     *     );
     * @param {string} old_version_html - html string to swagger json of an old version
     * @param {string} new_version_html - html string to swagger json of an new version
     * @param {Object[]} ignoreRuleIds - messages come with a ruleId to identify their type. array of ids to be ignored or else it could pollute the output
     * @event Swagger#ON_GRAPH
     * @event Swagger#ON_ERROR
     */
    makeGraph(old_version_html, new_version_html, ignoreRuleIds) {

        let old_version = Url.parse(old_version_html);
        let new_version = Url.parse(new_version_html);

        if (ignoreRuleIds === undefined)
            ignoreRuleIds = [];

        let gatherer = new Gatherer({
            old_version_swagger_data: null,
            new_version_swagger_data: null,
            diff_data: null
        });

        gatherer.once(Gatherer.ON_GATHERED, data => {

            let diff = data.diff_data;
            let relationships = SwaggerGraph.merge(
                new SwaggerGraph(JSON.parse(String(data.old_version_swagger_data))),
                new SwaggerGraph(JSON.parse(String(data.new_version_swagger_data)))
            );

            let messages = diff.warnings.concat(diff.infos.concat(diff.errors)).filter(message => !ignoreRuleIds.includes(message.ruleId));
            messages.forEach(message => {
                if (relationships.hasNode(message.key_name)) {
                    let node = relationships.getNode(message.key_name);
                    node.addMessage(message);
                }
                else
                    console.warn(Util.format('WARNING cannot find key={%s} in graph. Message: \n %o', message.key_name, message));
            });

            this.emit(Swagger.ON_GRAPH, relationships);
        });
        gatherer.once(Gatherer.ON_ERROR, message => this.emit(Swagger.ON_ERROR, message));

        let old_version_request = new Request();
        let new_version_request = new Request();

        old_version_request.on(Request.ON_DATA, data => gatherer.gather('old_version_swagger_data', data));
        old_version_request.on(Request.ON_ERROR, e => this.emit(Swagger.ON_ERROR, e));

        new_version_request.on(Request.ON_DATA, data => gatherer.gather('new_version_swagger_data', data));
        new_version_request.on(Request.ON_ERROR, e => this.emit(Swagger.ON_ERROR, e));

        this.once(Swagger.ON_DIFF, data => gatherer.gather('diff_data', data));

        old_version_request.get_data(old_version);
        new_version_request.get_data(new_version);
        this.diff(old_version.href, new_version.href);
    }

    /**
     * report
     * creates a html page of the relationship graph and changes
     * ex: swagger.makeGraph(
     *              'test.html'
     *              'https://api-wgie.wargaming.net/tools/swagger.json',
     *              'https://api-wgie.wargaming.net/tools/swagger.json',
     *              ['edit-description', 'edit-summary']
     *     );
     * @param {string} filename - html file name to write to. include ".html"
     * @param {string} old_version_html - html string to swagger json of an old version
     * @param {string} new_version_html - html string to swagger json of an new version
     * @param {Object[]} ignoreRuleIds - messages come with a ruleId to identify their type. array of ids to be ignored or else it could pollute the output
     * @event Swagger#ON_GRAON_WRITTENPH
     * @event Swagger#ON_ERROR
     */
    report(filename, old_version_html, new_version_html, ignoreRuleIds) {
        this.once(Swagger.ON_GRAPH, relationships => {

            let graph = relationships.graph;

            let page = new HTMLPageBuilder();
            page.stylize('html', "{font-family:'Roboto', sans-serif; color:#222222; background:#cccccd;}");
            page.stylize('h2', "{margin-bottom:1px;margin-top:1px;}");
            page.stylize('h3', "{color:#009f0a;margin-left:25px;margin-bottom:10px;}");
            page.stylize('h4', "{margin-bottom:1px;margin-top:1px;}");
            page.stylize('h5', "{margin-top:1px;}");
            page.stylize('div', "{margin-left:25px;}");
            page.stylize('details', "{margin-left:5px;}");
            page.stylize('pre', "{margin-top:1px; margin-bottom:5px}");

            let oldHeader = new Element('h2');
            oldHeader.content(Util.format('old: %s', old_version_html));
            page.nest(oldHeader);

            let newHeader = new Element('h2');
            newHeader.content(Util.format('new: %s', new_version_html));
            page.nest(newHeader);

            Object.keys(graph)
                .filter(key => graph[key].referencedBy.length === 0)
                .forEach(root => {

                    let table = new Element('table');
                    let rootNode = graph[root];

                    let header = new Element('h3');
                    header.content(Util.format('%s %s', JSON.stringify(rootNode.methods), root));
                    table.nest(header);

                    let total_messages = 0;
                    let queue = [{
                        name: root,
                        stack: [root],
                        node: rootNode,
                        report: table
                    }];

                    while (queue.length > 0) {

                        let item = queue.pop();

                        total_messages += item.node.messages.length;

                        item.node.messages.forEach(message => {

                            let style = {style: 'color:magenta'};
                            if (message.severity === 'info')
                                style = {style: 'color:#1083DF'};
                            else if (message.severity === 'warning')
                                style = {style: 'color:#e28924'};
                            else if (message.severity === 'error')
                                style = {style: 'color:#ed2323'};

                            let details = new Element('details');
                            details.attributes(style);

                            let summary = new Element('summary');
                            let font = new Element('font');
                            font.attributes(style);
                            font.content(Util.format('[%s] %s', message.severity, message.message));

                            summary.nest(font);
                            details.nest(summary);

                            let pre = new Element('pre');
                            pre.attributes(style);
                            pre.content(Util.format('%s', JSON.stringify(item.node.propertiesAndTypes, null, 4)));

                            details.nest(pre);

                            item.report.nest(details)
                        });

                        item.node.references.forEach(reference => {
                            if (item.stack.includes(reference))
                                return;

                            let newStack = item.stack.slice(0, item.stack.length);
                            newStack.push(reference);

                            let div = new Element('div');
                            div.content(reference);
                            item.report.nest(div);

                            queue.push({
                                name: reference,
                                stack: newStack,
                                node: graph[reference],
                                report: div
                            });
                        });
                    }

                    if (total_messages > 0)
                        page.nest(table);

                });
            Filesystem.writeFile(filename, page.toString(), err => {
                if (err) {
                    this.emit(Swagger.ON_ERROR);
                }
                this.emit(Swagger.ON_WRITTEN);
            });
        });
        this.makeGraph(old_version_html, new_version_html, ignoreRuleIds)
    }

    /**
     * diff
     * creates a diff between two swaggers using SwaggerDiff
     * ex: swagger.diff(
     *              'https://api-wgie.wargaming.net/tools/swagger.json',
     *              'https://api-wgie.wargaming.net/tools/swagger.json',
     *     );
     * @param {string} old_version_html - html string to swagger json of an old version
     * @param {string} new_version_html - html string to swagger json of an new version
     * @event Swagger#ON_DIFF
     */
    diff(old_version_html, new_version_html) {

        SwaggerDiff(old_version_html, new_version_html).then(diff => {

            //adds severity to each messages and adds key_name to message
            //key_name identifies which API object this message belongs to.
            //path and descriptionPath both signify this, but also adds extra stuff to the string. this just cleans that up.
            diff.warnings.forEach(warning => {
                warning['severity'] = 'warning';
                warning['key_name'] = Swagger.__createKeyName(warning);
            });
            diff.infos.forEach(info => {
                info['severity'] = 'info';
                info['key_name'] = Swagger.__createKeyName(info);
            });
            diff.errors.forEach(error => {
                error['severity'] = 'error';
                error['key_name'] = Swagger.__createKeyName(error);
            });

            this.emit(Swagger.ON_DIFF, diff);
        });
    }

}

module.exports = Swagger;