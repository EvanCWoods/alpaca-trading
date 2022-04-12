import time
import requests


# GLOBAL VARIABLES
HOUR = 3600


# Function to get the data from the api
def getDataFeed():
    data = requests.get("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD")
    return data.json()


# Recursive function to get the current unix timestamp
def getHours():
    currentTime = int(time.time())  # Get the current time as an interger

    if (currentTime % HOUR == 0):   # If the time is devisable by the number of seconds in an hour, it is a new hour
        print(getDataFeed())    # Print the data form the api
        time.sleep(1)
        getHours()
    else:   # If the current time is not a new hour, re run the function, adding a 1 second delay
        time.sleep(1)
        getHours()


getHours()