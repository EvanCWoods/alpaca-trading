# import time
# import requests
# from decouple import config

# # GLOBAL VARIABLES
# HOUR = 3600
# API_ENDPOINT = config("API_ENDPOINT")


# # Function to get the data from the api
# def getDataFeed():
#     data = requests.get(API_ENDPOINT)
#     return data.json()


# # Recursive function to get the current unix timestamp
# def getHours():
#     currentTime = int(time.time())  # Get the current time as an interger

#     if (currentTime % HOUR == 0):   # If the time is devisable by the number of seconds in an hour, it is a new hour
#         print(getDataFeed())    # Print the data form the api
#         time.sleep(1)
#         getHours()
#     else:   # If the current time is not a new hour, re run the function, adding a 1 second delay
#         time.sleep(1)
#         getHours()


# getHours()


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pprint 
from decouple import config
import os


API_KEY = config("API_KEY")
pp = pprint.PrettyPrinter(indent=4)

url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
print(url)
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}
parameters = {
'id':'1'

}

session = Session()
session.headers.update(headers)
try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    pp.pprint(data)
    

except (ConnectionError, Timeout, TooManyRedirects) as e:
    data = json.loads(response.text)
    pp.pprint(data)