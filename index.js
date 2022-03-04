const Alpaca = require('@alpacahq/alpaca-trade-api');
const _ = require("lodash");
const Indicators = require("technicalindicators");

const alpaca = new Alpaca({
    keyId: process.env.API_KEY,
    secretKey: process.env.SECRET_KEY,
    paper: true
})


class Interactions {
    async getAccount() {
        const account = await alpaca.getAccount();
        console.log(account);
        return account;
    }

    async getActivity() {
        const activity = await alpaca.getAccountActivities({
            activityTypes: ["FILL", "TRANS", "ACATC", "ACATS", "CSD", "CSW"],
            direction: "asc",
            pageSize: 100,
        });
        if (activity.length > 0) {
            console.log(activity);
            return activity;
        } else {
            console.log("No activity on this account yet...")
        }
    }
}

const app = new Interactions();
app.getAccount();
app.getActivity();