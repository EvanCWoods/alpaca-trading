const BTC = require("../models");


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

const useData = async () => {
    let sma = [];
    const data = await getData();
    for (let i = 9; i < data.length; i++) {
        sma.push(
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
            ) / 10;
    }
    console.log(sma);
}

useData();