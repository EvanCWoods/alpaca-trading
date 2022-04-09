from re import I
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt

# GLOBAL VARIABLES
FILE = "raw-data/BTC-Hourly.csv"
AVERAGE_LENGTH = 20
WINDOW_SIZE = 500


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


def getMa(prices, rate):
    return prices.rolling(rate).mean()


def testStrategy(signal, prices):
    CASH = 100
    BUY = True
    SELL = False
    i = 0
    while i < len(prices) and BUY == True:
        if (prices[i - 1] < signal[i - 1] and prices[i] > signal[i]):
            buyPrice = prices[i]
            BUY = False
            SELL = True
            n = i
            while n < len(prices) and SELL == True:
                if (prices[n - 1] > signal[n - 1] and prices[n] < signal[n]):
                    sellPrice = prices[n]
                    BUY = True
                    SELL = False
                    CASH = CASH * 1 + (sellPrice - buyPrice) / buyPrice
                    print({"CASH": CASH, "buyPrice": buyPrice, "sellPrice": sellPrice})
                n += 1
            i = n
        i += 1
    return CASH, i


# Main function
def main():
    print(
        testStrategy(
            np.array(getMa(getData(FILE), 20)).flatten(),
            np.array(getData(FILE)).flatten()))


if (__name__ == "__main__"):
    main()