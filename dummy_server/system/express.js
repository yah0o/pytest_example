const express = require('express');
const bodyParser = require('body-parser');
const fileUpload = require('express-fileupload');
const cors = require('cors');



class Express {

    create_server() {
        let server = express();
        server.use(bodyParser.json()); // for parsing application/json
        server.use(fileUpload());
        server.use((request, response, next) => {
            response.header("Access-Control-Allow-Origin", "*");
            response.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
            next();
        });
        return server;
    }

    create_router() {
        return express.Router();
    }
} module.exports = Express;