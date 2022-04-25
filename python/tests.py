from cProfile import label
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# GLOBAL VARIABLES
FILE = "raw-data/BTC-Hourly.csv"
RATE = 20
HISTORY = 700

# get the data from the CSV file
def getData():
  file = open(FILE)
  data = csv.reader(file)

  headers = []
  headers = next(data)

  rows = []
  for row in data:
    if (row[1] != "null"):
      rows.append(
      {
        # "Date": str(row[0]),
        # "Open": float(row[1]),
        # "High": float(row[2]),
        # "Low": float(row[3]),
        "Close": float(row[6])
      }
    )

  return rows


# get the close data
def getClose():
  close = []

  data = getData()
  for element in data:
    close.append(element.get("Close"))

  return pd.DataFrame(close)

close = getClose()

 
#  Get the average of a given window
def getAverage(windowSize):
  x = np.arange(0, len(close))
  moving_averages = []

  n = 0
  while n < windowSize:
    moving_averages.append(0)
    n+=1

  i = 0  
  # Loop through the array to consider
  # every window of size 3
  while i < len(close) - windowSize + 1:
    
    # Store elements from i to i+window_size
    # in list to get the current window
    window = close[i : i + windowSize]
  
    # Calculate the average of current window
    window_average = round(sum(window) / windowSize, 2)
      
    # Store the average of current
    # window in moving average list
    moving_averages.append(window_average)
    
    # Shift window to right by one position
    i += 1

  return moving_averages


def get_sma(prices, rate):
    return prices.rolling(rate).mean()

def get_bollinger_bands(prices, rate=RATE):
    sma = get_sma(prices, rate)
    std = prices.rolling(rate).std()
    bollinger_up = sma + std * 2 # Calculate top band
    bollinger_down = sma - std * 2 # Calculate bottom band
    return bollinger_up, bollinger_down


bollinger_up, bollinger_down = get_bollinger_bands(getClose())
sma = get_sma(getClose(), RATE)



def rsiIndex(periods = 10, ema = True):
    close_delta = pd.DataFrame(getClose()).diff()

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


# Function to get buy signals
def buySell(spot_price, sma, bollinger_up, bollinger_down):
  # Arrays to store buyy/sell indexes, buy/sell prices to be plotted later
  buys = []
  sells = []
  buy_price = []
  sell_price = []

  # Preprocess the data to be single dimension numpy arrays
  spot_price = np.array(spot_price).flatten()
  sma = np.array(sma).flatten()
  bollinger_up = np.array(bollinger_up).flatten()
  bollinger_down = np.array(bollinger_down).flatten()
  rsi = np.array(rsiIndex()).flatten()
  ema13 = np.array(pd.DataFrame(spot_price).ewm(span=13, adjust=False).mean()).flatten()
  ema26 = np.array(pd.DataFrame(spot_price).ewm(span=26, adjust=False).mean()).flatten()

  # Add None values to each array up to the point where the moving average is created (RATE value)
  n = 0
  while n < RATE:
    buys.append(None)
    buy_price.append(None)
    sell_price.append(None)
    sells.append(None)
    n+=1
  i = RATE
  while (i < len(spot_price)):
      # Get buy signals if the spot price is lower than the bottom bollinger band, rsi is lower than 30, and the 13 ema is below the 26 ema
    if ((spot_price[i-1] < bollinger_down[i-1] and spot_price[i] >= bollinger_down[i]) and (rsi[i] < 30)): #and (rsi[i-1] < 28 and rsi[i-1] < rsi[i]) and ema13[i] < ema26[i]):
      buys.append(i)
      buy_price.append(spot_price[i])
      # Get sell signals if the spot price is higher than the upper bollinger band, rsi is above 70, and the 13 ema is above the 26 ema
    elif (spot_price[i] > bollinger_up[i] and rsi[i] > 72 and ema13[i] > ema26[i]):
      sells.append(i)
      sell_price.append(spot_price[i])
    else:
      buy_price.append(None) # if the price is not above the bottom bollinger band add  None to the price (y)
      sell_price.append(None) # if the price is not above the bottom bollinger band add  None to the price (y)
      buys.append(None)  # if the price is not above the bottom bollinger band add None to the index (x)
      sells.append(None) # if the price is not above the bottom bollinger band add None to the index (x)
    i+=1
  
  return buys, sells, buy_price, sell_price


buys, sells, buy_price, sell_price = buySell(close, sma, bollinger_up, bollinger_down)
ema13 = np.array(pd.DataFrame(np.array(getClose()).flatten()).ewm(span=13, adjust=False).mean()).flatten()
ema26 = np.array(pd.DataFrame(np.array(getClose()).flatten()).ewm(span=26, adjust=False).mean()).flatten()

plot1 = plt.figure(1)
plt.title("BTC" + ' Bollinger Bands')
plt.xlabel('Days')
plt.ylabel('Closing Prices')
plt.plot(close[:HISTORY], label='Closing Prices', c="#000000")
plt.plot(bollinger_up[:HISTORY], label='Bollinger Up', c='#33C7FF', linewidth=1)
plt.plot(bollinger_down[:HISTORY], label='Bollinger Down', c='#33C7FF', linewidth=1)
plt.plot(get_sma(close[:HISTORY], RATE), label='SMA20', c='#808080', linewidth=1)
plt.scatter(buys[:HISTORY], buy_price[:HISTORY], marker="^", c="g", label="buys, spot price") # add ^ smbols when on buy signal 
plt.scatter(sells[:HISTORY], sell_price[:HISTORY], marker="v", c="r", label="sells, spot price") # add v smbols when on sell signal 
plt.legend()

plot2 = plt.figure(2)
plt.title("MACD")
plt.plot(np.arange(0, HISTORY), ema13[:HISTORY])
plt.plot(np.arange(0, HISTORY), ema26[:HISTORY])

plt3 = plt.figure(3)
plt.title("RSI")
plt.plot(np.arange(0, HISTORY), np.array([72] * HISTORY), c="b")
plt.plot(np.array(rsiIndex()).flatten()[:HISTORY:])
plt.plot(np.arange(0, HISTORY), np.array([28] * HISTORY), c="b")
plt.show()
# plt.savefig("public/images/btc-1h.png")


def main():
  return



if (__name__ == "__main__"):
  main()