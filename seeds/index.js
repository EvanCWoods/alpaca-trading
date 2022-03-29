const seedBtc = require("./seedBtc");

const sequelize = require("../config/connection");


const runSeeds = async() => {
    await sequelize.sync({force: true});
    await seedBtc();
    process.exit(0);
}

runSeeds();