//quick and dirty args parser
class ArgumentParser {

    constructor() {
        this.__argv = process.argv.splice(2, process.argv.length);
        if (this.__argv.includes('-h') || this.__argv.includes('--help'))
            this.help();

        this.__expected = {};

        this.addArgument('-h', 'string', 'help', false);
    }

    parse() {
        this.__argv.forEach(argument => {

            let kvp = argument.split('=');
            let key = kvp[0];
            let value = kvp[1];

            if (!this.__expected.hasOwnProperty(key)) {
                console.log(key);
                this.help();
            }

            this.__expected[key].value = value;
        });

        Object.keys(this.__expected).forEach(argument => {
            if (this.__expected[argument].required) {
                if (this.__expected[argument].value === null) {
                    console.log('missing', argument, 'is required');
                    this.help();
                }
            }
        });
    }

    getArgument(key) {
        let arg = this.__expected[key];
        if (arg.type === 'json' && typeof arg.value !== 'object')
            return JSON.parse(arg.value);
        return this.__expected[key].value;
    }

    addArgument(key, type, help, required, default_value) {

        let value = null;
        if (!required && default_value !== undefined)
            value = default_value;

        this.__expected[key] = {
            type: type,
            help: help,
            value: value,
            required: required
        }
    }

    help() {

        console.log('help: ');
        Object.keys(this.__expected).forEach(key => {
            console.log(key, ':', this.__expected[key].help);
        });
        process.exit(1);
    }
}

module.exports = ArgumentParser;
