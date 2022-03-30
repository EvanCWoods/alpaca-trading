const seedBtc = require("./seedBtc");
const seedTrend = require("./seedTrend");

const sequelize = require("../config/connection");


const runSeeds = async() => {
    await sequelize.sync({force: true});
    await seedBtc();
    await seedTrend();
    process.exit(0);
}

runSeeds();