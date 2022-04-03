import csv
import matplotlib.pyplot as plt
import numpy as np

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


# Average the data
def average():
  close = []

  data = getData()
  for element in data:
    close.append(element.get("Close"))

    x = np.arange(0, len(data))


  window_size = 10
  
  i = 0
  # Initialize an empty list to store moving averages
  moving_averages = [0,0,0,0,0,0,0,0,0]
  
  # Loop through the array to consider
  # every window of size 3
  while i < len(close) - window_size + 1:
    
    # Store elements from i to i+window_size
    # in list to get the current window
    window = close[i : i + window_size]
  
    # Calculate the average of current window
    window_average = round(sum(window) / window_size, 2)
      
    # Store the average of current
    # window in moving average list
    moving_averages.append(window_average)
    
    # Shift window to right by one position
    i += 1

  # showData(x, close, moving_averages)
  return moving_averages
  

# Show the data
def showData(x,y, average=None):
  if (average != None):
    plt.figure(figsize=(15, 8))
    plt.plot(x, y)
    plt.plot(x, average)
    plt.show()
  else:
    plt.figure(figsize=(15, 8))
    plt.plot(x, y)
    plt.show()
  


def main():
  average()


if (__name__ == "__main__"):
  main()