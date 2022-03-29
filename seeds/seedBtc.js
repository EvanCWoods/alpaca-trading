const csv = require("csv-parser");
const fs = require("fs");
const path = "../data";
const BTC = require("../models");

let data = [];

fs.createReadStream("seeds/BTC-AUD.csv")
  .pipe(csv())
  .on("data", (row) => {
    data.push(
        {
            open: row.Open,
            high: row.High,
            low: row.Low,
            close: row.Close,
            volume: row.Volume
        }
    );
  })
  .on("end", () => {
    console.log("CSV file successfully processed");
    console.log(data);
  });


const seedBtc = () => BTC.bulkCreate(data);

module.exports = seedBtc;