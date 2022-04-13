import time
from decouple import config
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os

# GLOBAL VARIABLES
HOUR = 3600
API_ENDPOINT = config("API_ENDPOINT")
API_KEY = config("API_KEY")


# Function to get the data from the api
def getDataFeed(path):
    url = path  # Set the path to the url
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,   # Add the api key for permissions
    }
    parameters = {'id': '1'}    # Get the bitcoin data
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data # Return the data object containing all of the content about bitcoin

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        data = json.loads(response.text)
        return data # Return the error message if something goes wrong


# Recursive function to get the current unix timestamp
def getHours():
    currentTime = int(time.time())  # Get the current time as an interger

    if (currentTime % HOUR == 0):   # If the time is devisable by the number of seconds in an hour, it is a new hour
        print(getDataFeed(API_ENDPOINT))    # Print the data form the api
        time.sleep(1)
        getHours()
    else:   # If the current time is not a new hour, re run the function, adding a 1 second delay
        time.sleep(1)
        getHours()


getHours()