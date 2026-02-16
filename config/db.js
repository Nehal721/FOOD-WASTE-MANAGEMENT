const {Client} = require("pg");

const SQL = `
CREATE TABLE IF NOT EXISTS users(
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    organization_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    password_hash VARCHAR(20) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ("donor", "receiver", "admin")),
    address TEXT NOT NULL,
    latitude NUMERIC(10, 6) NOT NULL,
    longitude NUMERIC(10, 6) NOT NULL,  
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    pin_code VARCHAR(10) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP  
);
`;

async function main(){
    const client = new Client({
        connectionString: "http://postgres:postgres@localhost:5432/fsm"
    });

    console.log("Seeding...");
    await client.connect();
    await client.query(SQL);
    await client.end();
    console.log("Done!");
}

main();