const {Pool} = require("pg");

const pool = new Pool({
    connectionString: "http://postgres:postgres@localhost:5432/fsm"
});

module.exports = pool;