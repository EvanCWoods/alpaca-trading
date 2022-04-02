import csv
import matplotlib.pyplot as plt
import numpy as np

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


def showData():
  close = []

  data = getData()
  for element in data:
    close.append(element.get("Close"))

  x = np.arange(0, len(close))
  plt.plot(x, close)
  plt.show()
  


def main():
  showData()


if (__name__ == "__main__"):
  main()