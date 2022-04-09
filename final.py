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

    return pd.DataFrame(rows[::-1])


#  Get the average of a given window
def getSma(prices, rate):
    return prices.rolling(rate).mean()

# Function to get the bollinger bands
def getBollingerBands(prices, rate=AVERAGE_LENGTH):
    sma = getSma(prices, rate)
    std = prices.rolling(rate).std()
    bollinger_up = sma + std * 2 # Calculate top band
    bollinger_down = sma - std * 2 # Calculate bottom band
    return bollinger_up, sma, bollinger_down

# Function to get the RSI
def rsiIndex(periods = 14, ema = True):
    close_delta = pd.DataFrame(getData(FILE)).diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    if ema == True:
	    # Use exponential moving average
        ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
        ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window = periods, adjust=False).mean()
        ma_down = down.rolling(window = periods, adjust=False).mean()
        
    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    return rsi


# Function to check if the price is above the bollinger Bands
def checkBollingerUp(price, bollingerUp):
    if (price > bollingerUp):
        return True
    else:
        return False
# Function to check if the price is above 70 on RSI
def checkRsiUp(rsi):
    if (rsi > 70):
        return True 
    else:
        return False
# Function to check if the 12 EMA is above the 26 ema on the macd
# Function to check if the price is below the bollinger Bands
def checkBollingerDown(price, bollingerDown):
    if (price < bollingerDown):
        return True
    else:
        return False
# Function to check if the price is below 30 on RSI
def checkRsiDown(rsi):
    if (rsi < 30):
        return True 
    else:
        return False
# Function to check if the 12 EMA is below the 26 ema on the macd'


# Function to get buy signals
def getSell():
    sells = []
    sellPrice = []
    buys = []
    buyPrice = []

    price = getData(FILE)
    bollinger_up, sma, bollinger_down = getBollingerBands(price)
    rsi = rsiIndex()
    
    price = np.array(price).flatten()
    bollinger_up = np.array(bollinger_up).flatten()
    bollinger_down = np.array(bollinger_down).flatten()
    rsi = np.array(rsi).flatten()
    i = 0
    while i < len(price):
        bollingerSells = checkBollingerUp(price[i], bollinger_up[i])
        bollingerBuys = checkBollingerDown(price[i], bollinger_down[i])
        rsiSells = checkRsiUp(rsi[i])
        rsiBuys = checkRsiDown(rsi[i])
        if (bollingerSells == True and rsiSells == True):
            sells.append(i)
            sellPrice.append(price[i])
        elif (bollingerBuys == True and rsiBuys == True):
            buys.append(i)
            buyPrice.append(price[i])
        else:
            sells.append(None)
            sellPrice.append(None)
            buys.append(None)
            buyPrice.append(None)
        i+=1

    return sells, sellPrice, buys, buyPrice


### 
# The above should sequentially check the viability of a position and if all conditions are met, 
# return a buy or sell signal 
###


# Main function
def main():
    close = np.array(getData(FILE)).flatten()
    bollinger_up, sma, bollinger_down = getBollingerBands(getData(FILE))
    rsi = rsiIndex()
    sells, sellPrice, buys, buyPrice = getSell()
    sells = np.array(sells).flatten()
    sellPrice = np.array(sellPrice).flatten()
    buys = np.array(buys).flatten()
    buyPrice = np.array(buyPrice).flatten()

    print(len(close), len(sells), len(sellPrice), len(buys), len(buyPrice))

    plt.figure(figsize=(10,7))
    plt.plot(np.arange(0, len(close[-WINDOW_SIZE:])), close[-WINDOW_SIZE:], c="#000")
    plt.plot(np.arange(0, len(close[-WINDOW_SIZE:])), bollinger_up[-WINDOW_SIZE:], c="grey", label="bollinger band")
    plt.plot(np.arange(0, len(close[-WINDOW_SIZE:])), sma[-WINDOW_SIZE:], c="grey", label="sma")
    plt.plot(np.arange(0, len(close[-WINDOW_SIZE:])), bollinger_down[-WINDOW_SIZE:], c="grey")
    plt.scatter(np.arange(0, len(sells[-WINDOW_SIZE:])), sellPrice[-WINDOW_SIZE:], marker="v", c="r")
    plt.scatter(np.arange(0, len(buys[-WINDOW_SIZE:])), buyPrice[-WINDOW_SIZE:], marker="^", c="g")
    plt.legend()

    plt.figure(figsize=(10, 7))
    plt.plot(np.arange(0, len(rsi[-WINDOW_SIZE:])), np.array([70] * len(rsi[-WINDOW_SIZE:])))
    plt.plot(np.arange(0, len(rsi[-WINDOW_SIZE:])), rsi[-WINDOW_SIZE:])
    plt.plot(np.arange(0, len(rsi[-WINDOW_SIZE:])), np.array([30] * len(rsi[-WINDOW_SIZE:])))

    plt.show()


if (__name__ == "__main__"):
    main()