# APIs for data from exchanges

import requests

# -- Gemini Notes --
# https://docs.gemini.com/rest-api/#symbols
# https://api.gemini.com/v1/symbols/details/btcusd
# https://api.gemini.com/v1/pubticker/:symbol
# https://api.gemini.com/v1/pricefeed

GEMINI_BASE_URL = 'https://api.gemini.com'


def get_gemini_asset_price(symbol):
    """Identifies current asset price on Gemini.
    :arg symbol: string for trading pair {btcusd|ethusd}

    :returns: dict with bid/ask/latest for top level symbol key
    """
    url = '{}/v1/publicticker/{}'.format(GEMINI_BASE_URL, symbol)
    resp = requests.get(url)
    resp_data = resp.json()
    ret = {}
    ret[symbol] = {
        'bid': resp_data.get('bid'),
        'ask': resp_data.get('ask'),
        'latest': resp_data.get('latest')
    }

    return ret


# -- Okcoin Notes --
# https://www.okcoin.com/docs/en/
# https://www.okcoin.com/api/spot/v3/instruments/BTC-USD/book
# https://www.okcoin.com/api/spot/v3/instruments/BTC-USD/candles


# -- Binance.US Notes --
# https://docs.binance.us/#introduction
# The base endpoint is: https://api.binance.us
# https://api.binance.us/api/v3/ticker/price?symbol=BTCUSD
# https://api.binance.us/api/v3/ticker/price?symbol=ETHUSD


# -- Coinbase Notes --
# https://docs.cloud.coinbase.com/exchange/docs#get-historic-rates
# Requires exchange account API - might be free if one has a Coinbase account
# https://api.exchange.coinbase.com/products/{product_id}/ticker


# -- FTX.US Notes --
# https://docs.ftx.us/#overview
# https://ftx.us/api/markets
# https://ftx.us/api/markets/BTC/USD
