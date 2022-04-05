from cProfile import label
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# get the data from the CSV file
def getData():
  file = open("BTC-USD.csv")
  data = csv.reader(file)

  headers = []
  headers = next(data)

  rows = []
  for row in data:
    if (row[1] != "null"):
      rows.append(
      {
        "Date": str(row[0]),
        "Open": float(row[1]),
        "High": float(row[2]),
        "Low": float(row[3]),
        "Close": float(row[4])
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

 
#  Get the average of a given window
def getAverage(windowSize):
  data = getClose()
  x = np.arange(0, len(data))
  moving_averages = []

  n = 0
  while n < windowSize:
    moving_averages.append(0)
    n+=1

  i = 0  
  # Loop through the array to consider
  # every window of size 3
  while i < len(data) - windowSize + 1:
    
    # Store elements from i to i+window_size
    # in list to get the current window
    window = data[i : i + windowSize]
  
    # Calculate the average of current window
    window_average = round(sum(window) / windowSize, 2)
      
    # Store the average of current
    # window in moving average list
    moving_averages.append(window_average)
    
    # Shift window to right by one position
    i += 1

  return moving_averages
  

# Show the data
def showData(x,y, average1=None, average2=None):
  if (average1 != None or average2 != None):
    plt.figure(figsize=(15, 8))
    plt.plot(x[-300:], y[-300:], label="Close")
    plt.plot(x[-300:], average1[-300:], label=" 10 day Average")
    plt.plot(x[-300:], average2[-300:], label=" 5 day Average")
    plt.legend(loc="upper left")
    plt.show()
  else:
    plt.figure(figsize=(15, 8))
    plt.plot(x, y)
    plt.show()
  




def get_sma(prices, rate):
    return prices.rolling(rate).mean()

def get_bollinger_bands(prices, rate=20):
    sma = get_sma(prices, rate)
    std = prices.rolling(rate).std()
    bollinger_up = sma + std * 2 # Calculate top band
    bollinger_down = sma - std * 2 # Calculate bottom band
    return bollinger_up, bollinger_down


bollinger_up, bollinger_down = get_bollinger_bands(getClose())
sma = get_sma(getClose(), 20)


# Function to get buy signals
def buySell(spot_price, sma, bollinger_up, bollinger_down):
  buys = []
  sells = []
  buy_price = []
  sell_price = []
  spot_price = np.array(spot_price).flatten()
  sma = np.array(sma).flatten()
  bollinger_up = np.array(bollinger_up).flatten()
  bollinger_down = np.array(bollinger_down).flatten()

  n = 0
  while n < 20:
    buys.append(None)
    buy_price.append(None)
    sell_price.append(None)
    sells.append(None)
    n+=1
  # Loop through and check if the spot price is lower than the bottom bollinger band (starting at 20 for consistency of data location)
  i = 0
  while (i < len(spot_price)):
    if (spot_price[i] < bollinger_down[i]):
      buys.append(i)
      buy_price.append(spot_price[i])
    elif (spot_price[i] > bollinger_up[i]):
      sells.append(i)
      sell_price.append(spot_price[i])
    else:
      buy_price.append(None) # if the price is not above the bottom bollinger band add  None to the price (y)
      sell_price.append(None) # if the price is not above the bottom bollinger band add  None to the price (y)
      buys.append(None)  # if the price is not above the bottom bollinger band add None to the index (x)
      sells.append(None)
    i+=1
  
  return buys, sells, buy_price, sell_price

buys, sells, buy_price, sell_price = buySell(getClose(), sma, bollinger_up, bollinger_down)

plt.title("BTC" + ' Bollinger Bands')
plt.xlabel('Days')
plt.ylabel('Closing Prices')
plt.plot(getClose()[-300:], label='Closing Prices', c="#000000")
plt.plot(bollinger_up[-300:], label='Bollinger Up', c='#33C7FF', linewidth=1)
plt.plot(bollinger_down[-300:], label='Bollinger Down', c='#33C7FF', linewidth=1)
plt.plot(get_sma(getClose()[-300:], 20), label='SMA20', c='#808080', linewidth=1)
plt.scatter(buys[-300:], buy_price[-300:], marker="^", c="g", label="buys, spot price") # add ^ smbols when on buy signal 
plt.scatter(sells[-300:], sell_price[-300:], marker="v", c="r", label="sells, spot price") # add ^ smbols when on buy signal 
plt.legend()
plt.show()


def main():
  y = getClose()
  x = np.arange(0, len(y))
  # showData(x, y, bollinger_down, bollinger_up)



if (__name__ == "__main__"):
  main()