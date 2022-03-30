const {Trend} = require("../models");
const data = require("../data.json");

const seedTrend = () => Trend.bulkCreate(data);

module.exports = seedTrend;