import time
import requests
from pymongo import MongoClient
import ssl
import sys
import os
from decouple import config
from datetime import datetime
import matplotlib.pyplot as plt


def getDataFeed(CONNECTION_STRING):

    cluster = MongoClient(CONNECTION_STRING,
        ssl_cert_reqs=ssl.CERT_NONE)
    db = cluster["data"]
    return db.live


col = list(getDataFeed(config("MONGO_URI")).find({}).sort("timestamp", 1))

timestamps = []
price = []

for item in col:
    # print(datetime.fromtimestamp(item.timestamp))
    timestamps.append(datetime.fromtimestamp(item["timestamp"]))
    price.append(item["Close"])
    print(datetime.fromtimestamp(item["timestamp"]))


# plt.figure(figsize=(10,7))
# plt.plot(timestamps, price)
# plt.show()