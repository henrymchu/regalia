# Module for acquiring data from coinmarketcap/coingecko APIs

# What websites have API access to get data?
#     1. Are there rate limits to how often we can hit the service for information?

# What types of APIs are available to get ...
#     1. List of all assets available at a specific exchange
#     2. List of all exchanges that support a specific asset or trading pair

# Notes
#     1. https://www.coingecko.com/en/api
#         a. https://github.com/man-c/pycoingecko
#     2. https://coinmarketcap.com/api/

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def get_coinmarketcap_data(asset_symbol):

    url = 'https://sandbox-api.coinmarketcap.com/v2/cryptocurrency/market-pairs/latest'

    parameters = {
    'start':'1',
    'limit':'5000',
    'convert':'USD',
    "symbol": asset_symbol,
    }

    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        print(data)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)