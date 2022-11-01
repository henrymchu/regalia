# APIs for data from exchanges

import requests

from ticker_constants import (
    KNOWN_FTX_US_ASSETS,
    KNOWN_GEMINI_ASSETS,
)

BINANCE_US_BASE_URL = 'https://api.binance.us'
COINBASE_BASE_URL = 'https://api.exchange.coinbase.com'
CRYPTO_COM_BASE_URL = 'https://api.crypto.com'
FTX_US_BASE_URL = 'https://ftx.us'
GEMINI_BASE_URL = 'https://api.gemini.com'
KRAKEN_BASE_URL = 'https://api.kraken.com'
KUCOIN_BASE_URL = 'https://api.kucoin.com'
OKCOIN_BASE_URL = 'https://www.okcoin.com'


# -- Gemini Notes --
# https://docs.gemini.com/rest-api/#symbols
# https://api.gemini.com/v1/symbols/details/btcusd
# https://api.gemini.com/v1/pubticker/:symbol
# https://api.gemini.com/v1/pricefeed


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


def get_gemini_usd_trading_pairs():
    """Identifies all assets trading on Gemini against US dollar.

    :returns: list of tickers
    """
    url = '{}/v1/pricefeed'.format(GEMINI_BASE_URL)
    resp = requests.get(url)
    resp_data = resp.json()
    usd_assets = []
    gusd_assets = []
    btc_assets = []
    eth_assets = []
    eur_assets = []
    gbp_assets = []
    sgd_assets = []
    for pair_info in resp_data:
        raw = pair_info.get('pair')

        # Setup string slices for comparison
        remove_last_three = raw[:-3]
        last_three = raw[-3:]
        remove_last_four = raw[:-4]
        last_four = raw[-4:]

        if last_three == 'USD' and remove_last_three in KNOWN_GEMINI_ASSETS:
            ticker = remove_last_three
            usd_assets.append(ticker)
        elif last_four == 'GUSD' and remove_last_four in KNOWN_GEMINI_ASSETS:
            ticker = remove_last_four
            gusd_assets.append(ticker)
        elif last_three == 'BTC' and remove_last_three in KNOWN_GEMINI_ASSETS:
            ticker = remove_last_three
            btc_assets.append(ticker)
        elif last_three == 'ETH' and remove_last_three in KNOWN_GEMINI_ASSETS:
            ticker = remove_last_three
            eth_assets.append(ticker)
        elif last_three == 'EUR' and remove_last_three in KNOWN_GEMINI_ASSETS:
            ticker = remove_last_three
            eur_assets.append(ticker)
        elif last_three == 'GBP' and remove_last_three in KNOWN_GEMINI_ASSETS:
            ticker = remove_last_three
            gbp_assets.append(ticker)
        elif last_three == 'SGD' and remove_last_three in KNOWN_GEMINI_ASSETS:
            ticker = remove_last_three
            sgd_assets.append(ticker)
        elif last_three in ['BCH', 'DAI', 'LTC', 'FIL']:
            # Don't worry about trading pairs with bitcoin cash, dai, litecoin, or filecoin
            pass
        else:
            print('Unknown Gemini trading pair encountered: {}'.format(raw))

    return usd_assets



# -- Okcoin Notes --
# https://www.okcoin.com/docs/en/
# https://www.okcoin.com/api/spot/v3/instruments/BTC-USD/book
# https://www.okcoin.com/api/spot/v3/instruments/BTC-USD/candles
# https://www.okcoin.com/api/spot/v3/instruments/SCRT-USD/candles


def get_okcoin_usd_trading_pairs():
    """Identifies all assets trading on Okcoin against US dollar.

    :returns: list of tickers
    """
    pass  # TOOD

# -- Binance.US Notes --
# https://docs.binance.us/#introduction
# The base endpoint is: https://api.binance.us
# https://api.binance.us/api/v3/ticker/price?symbol=BTCUSD
# https://api.binance.us/api/v3/ticker/price?symbol=ETHUSD


def get_binance_us_usd_trading_pairs():
    """Identifies all assets trading on Binance.US against US dollar.

    :returns: list of tickers
    """
    pass  # TOOD


# -- Coinbase Notes --
# https://docs.cloud.coinbase.com/exchange/docs#get-historic-rates
# Requires exchange account API - might be free if one has a Coinbase account
# https://api.exchange.coinbase.com/products/{product_id}/ticker


def get_coinbase_usd_trading_pairs():
    """Identifies all assets trading on Coinbase against US dollar.

    :returns: list of tickers
    """
    pass  # TOOD


# -- FTX.US Notes --
# https://docs.ftx.us/#overview
# https://ftx.us/api/markets
# https://ftx.us/api/markets/BTC/USD


def get_ftx_us_usd_trading_pairs():
    """Identifies all assets trading on FTX.US against US dollar.

    :returns: list of tickers
    """
    url = '{}/api/markets'.format(FTX_US_BASE_URL)
    resp = requests.get(url)
    data = resp.json()
    if not data.get('success'):
        print('failed to get a successful response from https://ftx.us/api/markets')

    usd_assets = []
    results = data['result']
    for result in results:
        raw_name = result.get('name')
        pair = raw_name.split('/')
        if pair[1] == 'USD' and pair[0] not in KNOWN_FTX_US_ASSETS:
            print('Unknown FTX trading pair encountered: {}'.format(raw_name))
        elif pair[1] == 'USD':
            usd_assets.append(pair[0])

    return usd_assets


# -- Crypto.com Notes --
# https://exchange-docs.crypto.com/spot/index.html#introduction
# https://api.crypto.com/v2/public/get-instruments
# https://api.crypto.com/v2/public/get-ticker?instrument_name=BTC_USDT


# -- Kucoin Notes --
# https://docs.kucoin.com/#general
# https://api.kucoin.com/api/v2/symbols
# https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=BTC-USDT
# https://api.kucoin.com/api/v1/market/allTickers


# -- Kraken Notes --
# https://docs.kraken.com/rest/
# https://api.kraken.com/0/public/Ticker?pair=BTCUSD


def get_kraken_usd_trading_pairs():
    """Identifies all assets trading on Kraken against US dollar.

    :returns: list of tickers
    """
    pass  # TOOD
