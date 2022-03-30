const fs =require("fs");
const {BTC} = require("../models");


const getData = async () => {
    let dataList = [];
    try {
        const data = await BTC.findAll();

        for (let i = 0; i < data.length; i++) {
            dataList.push(data[i].dataValues);
        }
        return dataList;
    } catch (err) {
        console.log(err);
    }
    return dataList;
};

const getMA = async () => {
    let sma = [];
    const data = await getData();
    for (let i = 9; i < data.length; i++) {
        sma.push((
            data[i].close + 
            data[i-1].close + 
            data[i-2].close + 
            data[i-3].close + 
            data[i-4].close + 
            data[i-5].close + 
            data[i-6].close + 
            data[i-7].close + 
            data[i-8].close + 
            data[i-9].close
            ) / 10);
    }
    return sma;
}

const signals = async () => {
    let buyArray = [];
    let sellArray = [];
    // Get the sma and the raw data objects
    const sma = await getMA()
    let data = await getData();
    // cut the first 10 data points to match the sma length
    let cutData = data.splice(9);

    // loop through all data and return values of interest
    for (let i = 0; i < cutData.length; i++) {
        if ((cutData[i].close > sma[i] && sma[i] - sma[i-3] > 10)) {
            buyArray.push(cutData[i]);
        }
    }
    return buyArray;
}


const main = async () => {
    const data = await signals();
    console.log(data);
        fs.appendFile("data.json", JSON.stringify(data), (err) => {
            if (err) {
                console.log(err);
            } 
        });
}

main();