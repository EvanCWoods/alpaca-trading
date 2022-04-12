from pymongo import MongoClient
import csv
import numpy as np
import pandas as pd
from decouple import config

FILE = config("DATA")

client = MongoClient("localhost", 27017)

db = client["myDatabase"]
collection = db["raw-data"]

print(FILE)

file = open(f"./{FILE}")
data = csv.reader(file)

# Remove the header text from the file
headers = []
headers = next(data)

# Add each value to the rows array
rows = []
for row in data:
    rows.append(row)

sortedData = np.array(pd.DataFrame(rows[::-1]))  # Reverse the data to be past -> present

print(sortedData)

sortedRows = []
for row in sortedData:
    sortedRows.append(
         {
            "Timestamp": int(row[0]),
            "Date": str(row[1]),
            "Symbol": str(row[2]),
            "Open": float(row[3]),
            "High": float(row[4]),
            "Low": float(row[5]),
            "Close": float(row[6]),
            "Volume": float(row[7])
        }
    )

i = 0
while i < len(sortedRows):
    collection.insert_one(sortedRows[i])
    i+=1
