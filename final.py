from re import I
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
from decouple import config

# GLOBAL VARIABLES
FILE = config("DATA")

# Function to get the data from the file
def getData(source):
    file = open(source)
    data = csv.reader(file)

    # Remove the header text from the file
    headers = []
    headers = next(data)

    # Add each value to the rows array
    rows = []
    for row in data:
        if (row[1] != "null"):
            rows.append(float(row[6]))

    return pd.DataFrame(rows[::-1])  # Reverse the data to be past -> present


# Function to get the simple moving average
def getMa(prices, rate):
    return prices.rolling(rate).mean()

# Function to test the strategy
def testStrategy(average, prices):
    CASH = 100
    BUY = True
    SELL = False
    i = 0
    while i < len(prices) and BUY == True:
        if (prices[i - 1] < average[i - 1] and prices[i] > average[i]):
            buyPrice = prices[i]
            BUY = False
            SELL = True
            n = i
            while n < len(prices) and SELL == True:
                if (prices[n - 1] > average[n - 1] and prices[n] < average[n]):
                    sellPrice = prices[n]
                    BUY = True
                    SELL = False
                    roi = 1 + (sellPrice - buyPrice) / buyPrice
                    CASH = CASH * roi
                    print({"CASH": CASH, "buyPrice": buyPrice, "sellPrice": sellPrice, "ROI": roi, "Buy Index": i, "Sell Index": n})
                n += 1
            i = n
        i += 1
    summary = {"STARTING BALANCE": 100, "ENDING BALANCE": CASH, "PROFIT": CASH - 100, "ROI": (CASH / 100) * 100}
    return CASH, i, summary


# Main function
def main():
    print()
    print()
    print(
        testStrategy(
            np.array(getMa(getData(FILE), 200)).flatten(),
            np.array(getData(FILE)).flatten()))
    print()
    print()


if (__name__ == "__main__"):
    main()