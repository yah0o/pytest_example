const EventEmitter = require('events');

/**
 * a class that allows data to be gathered from many different calls so they can be executed async
 *  the data it knows it needs are passed in a json object with keys that have null
 *
 *      ex : let g = Gatherer({test1: null, test2: null});
 *
 *  when the data is set, Gatherer will emit an Gatherer.ON_GATHERED event with the initial json object filled out
 *
 *      ex: g.gather('test1', some_data);
 *
 *  g.gather('test2', some_other_data); -> will emit Gatherer.ON_GATHERED here
 *  ON_GATHERED will have the initial json object filled out
 *
 *  ex: g.once(Gatherer.ON_GATHERED, data => {
 *      console.log(data.test1); //will print some_data
 *      console.log(data.test2); //will print some_other_data
 *      });
 *
 */
class Gatherer extends EventEmitter {

    /**
     * @param {object} object
     */
    constructor(object) {
        super();

        this.__object = object;
        this.__emitted = false;
    }

    static get ON_GATHERED() {
        return 'on_gathered';
    }

    static get ON_ERROR() {
        return 'on_error';
    }

    /**
     * @param {string} key
     * @param value
     * @event Gatherer#ON_GATHERED
     * @event Gatherer#ON_ERROR
     */
    gather(key, value) {

        if (this.__emitted) {
            this.emit(Gatherer.ON_ERROR, 'Cannot set value of an already emitted builder');
            return;
        }

        this.__object[key] = value;
        if (Object.keys(this.__object).every(key => !!this.__object[key])) {
            this.emit(Gatherer.ON_GATHERED, this.__object)
        }
    }
}

module.exports = Gatherer;