# APIs for data from exchanges

# Python imports
import collections
# TODO Figure out how these imports work to not have to use sys.path.append
import json.decoder
import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from constants import (
    BINANCE_US_ID,
    COINBASE_ID,
    GEMINI_ID,
    KRAKEN_ID,
    OKCOIN_ID,
)

# Third party imports
import requests

# Local imports
from ticker_constants import (
    KNOWN_BINANCE_US_ASSETS,
    KNOWN_COINBASE_ASSETS,
    KNOWN_GEMINI_ASSETS,
    KNOWN_KRAKEN_ASSETS,
    KNOWN_OKCOIN_ASSETS,
)


BINANCE_US_BASE_URL = 'https://api.binance.us'
COINBASE_BASE_URL = 'https://api.exchange.coinbase.com'
CRYPTO_COM_BASE_URL = 'https://api.crypto.com'
GEMINI_BASE_URL = 'https://api.gemini.com'
KRAKEN_BASE_URL = 'https://api.kraken.com'
KUCOIN_BASE_URL = 'https://api.kucoin.com'
OKCOIN_BASE_URL = 'https://www.okcoin.com'


def convert_ticker_to_symbol(ticker, exchange_id):
    """Converts a ticker to a symbol for url insertion.
    :arg: ticker: str
    :arg: exchange_id: str

    :returns: str
    """
    url_symbol = ''
    if exchange_id in [BINANCE_US_ID, KRAKEN_ID]:
        url_symbol = '{}USD'.format(ticker.upper())
    elif exchange_id in [COINBASE_ID, OKCOIN_ID]:
        url_symbol = '{}-USD'.format(ticker.upper())
    elif exchange_id == GEMINI_ID:
        url_symbol = '{}usd'.format(ticker.lower())
    else:
        print('Invalid exchange identifier')

    return url_symbol


def get_asset_price_at_exchange(ticker, exchange_id):
    """Finds the current price of an asset at an exchange.
    :arg: ticker: str
    :arg: exchange_id: str

    :returns: price: float
    """
    symbol = convert_ticker_to_symbol(ticker, exchange_id)
    if exchange_id == BINANCE_US_ID:
        price_info = get_binance_us_asset_price(symbol)
        return price_info.get('price')
    elif exchange_id == COINBASE_ID:
        price_info = get_coinbase_asset_price(symbol)
        return price_info.get('price')
    elif exchange_id == GEMINI_ID:
        price_info = get_gemini_asset_price(symbol)
        return price_info.get('last')
    elif exchange_id == KRAKEN_ID:
        price_info = get_kraken_asset_price(symbol)
        return price_info.get('price')
    elif exchange_id == OKCOIN_ID:
        price_info = get_okcoin_asset_price(symbol)
        return price_info.get('close')
    else:
        print('Invalid exchange identifier')
        return None


def get_asset_order_book_at_exchange(ticker, exchange_id):
    """Finds the order book of an asset at an exchange.
    :arg: ticker: str
    :arg: exchange_id: str

    :returns: dict with min_ask/max_bid/dollar_value_min_asks/dollar_value_of_max_bids
    """
    symbol = convert_ticker_to_symbol(ticker, exchange_id)
    if exchange_id == BINANCE_US_ID:
        # TODO
        return {'min_ask': None, 'min_bid': None, 'dollar_value_min_asks': None, 'dollar_value_max_bids': None}
    elif exchange_id == COINBASE_ID:
        return get_coinbase_order_book(symbol)
    elif exchange_id == GEMINI_ID:
        return get_gemini_order_book(symbol)
    elif exchange_id == KRAKEN_ID:
        # TODO
        return {'min_ask': None, 'min_bid': None, 'dollar_value_min_asks': None, 'dollar_value_max_bids': None}
    elif exchange_id == OKCOIN_ID:
        return get_okcoin_order_book(symbol)


# -- Gemini Notes --
# https://api.gemini.com/v1/symbols/details/btcusd
# https://api.gemini.com/v1/pubticker/:symbol


def get_gemini_asset_price(symbol):
    """Identifies current asset price on Gemini.
    :arg symbol: string for trading pair {btcusd|ethusd}

    :returns: dict with bid/ask/last
    """
    url = '{}/v1/pubticker/{}'.format(GEMINI_BASE_URL, symbol)
    resp = requests.get(url)
    resp_data = resp.json()
    try:
        bid = float(resp_data.get('bid'))
        ask = float(resp_data.get('ask'))
        last = float(resp_data.get('last'))
    except TypeError:
        print('!!!!! Error in get_gemini_asset_price for {}'.format(symbol))
        bid = None
        ask = None
        last = None

    ret = {
        'bid': bid,
        'ask': ask,
        'last': last,
    }
    return ret


def get_gemini_order_book(symbol, size=5):
    """Retrieves details on Gemini order book for a single asset.
    :arg symbol: string for trading pair {btcusd|ethusd}
    :arg size: int

    :returns: dict with min_ask/max_bid/dollar_value_min_asks/dollar_value_of_max_bids
    """
    url = '{}/v1/book/{}'.format(GEMINI_BASE_URL, symbol)
    return get_order_book_helper(url, size, price_key='price', amount_key='amount')


def get_gemini_usd_trading_pairs():
    """Identifies all assets trading on Gemini against US dollar.

    :returns: list of tickers

    Notes:
        https://docs.gemini.com/rest-api/#symbols
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

    _ = check_for_delisting(KNOWN_GEMINI_ASSETS, usd_assets, 'Gemini')
    return usd_assets


def get_okcoin_asset_price(symbol):
    """Identifies current asset price on Okcoin.
    :arg symbol: string for trading pair {BTC-USD|ETH-USD}

    :returns: dict with open/high/low/close/volume
    """
    url = '{}/api/spot/v3/instruments/{}/candles'.format(OKCOIN_BASE_URL, symbol)
    resp = requests.get(url)
    resp_data = resp.json()
    if type(resp_data) == dict:
        print('okcoin {} dict resp: {}'.format(symbol, resp_data))
        return {}

    latest_candlesticks = resp_data[0]
    try:
        open_ = float(latest_candlesticks[1])
        high = float(latest_candlesticks[2])
        low = float(latest_candlesticks[3])
        close = float(latest_candlesticks[4])
        volume = float(latest_candlesticks[5])
    except TypeError:
        print('!!!!! Error in get_okcoin_asset_price for {}'.format(symbol))
        open_ = high = low = close = volume = None

    ret = {
        'open': open_,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume,
    }

    return ret


def get_okcoin_order_book(symbol, size=5):
    """Retrieves details on an Okcoin order book for a single asset.
    :arg symbol: string for trading pair {BTC-USD|ETH-USD}
    :arg size: int

    :returns: dict with min_ask/max_bid/dollar_value_min_asks/dollar_value_of_max_bids
    """
    url = '{}/api/spot/v3/instruments/{}/book?size={}'.format(OKCOIN_BASE_URL, symbol, size)
    return get_order_book_helper(url, size)


def get_okcoin_usd_trading_pairs():
    """Identifies all assets trading on Okcoin against US dollar.

    :returns: list of tickers

    Notes:
        Public API rate limit: 20 Requests per 2 seconds
        https://www.okcoin.com/docs/en/
        https://www.okcoin.com/api/spot/v3/instruments/BTC-USD/book
        https://www.okcoin.com/api/spot/v3/instruments/BTC-USD/candles
    """
    url = '{}/api/spot/v3/instruments/'.format(OKCOIN_BASE_URL)
    resp = requests.get(url)
    resp_data = resp.json()
    usd_assets = []
    for result in resp_data:
        base_currency = result.get('base_currency')
        quote_currency = result.get('quote_currency')
        if quote_currency == 'USD' and base_currency in KNOWN_OKCOIN_ASSETS:
            usd_assets.append(base_currency)
        elif quote_currency == 'USD':
            print('Unknown Okcoin USD trading pair encountered: {}'.format(base_currency))

    _ = check_for_delisting(KNOWN_OKCOIN_ASSETS, usd_assets, 'Okcoin')
    return usd_assets


def get_binance_us_asset_price(symbol):
    """Identifies current asset price on Binance.US.
    :arg symbol: string for trading pair {BTCUSD|ETHUSD}

    :returns: dict with symbol/price
    """
    url = '{}/api/v3/ticker/price?symbol={}'.format(BINANCE_US_BASE_URL, symbol)
    resp = requests.get(url)
    resp_data = resp.json()
    try:
        price = float(resp_data.get('price'))
    except TypeError:
        print('!!!!! Error in get_binance_us_asset_price for {}'.format(symbol))
        price = None

    ret = {
        'symbol': resp_data.get('symbol'),
        'price': price,
    }
    return ret


def get_binance_us_order_book(symbol, size=5):
    """Retrieves details on an Binance.US order book for a single asset.
    :arg symbol: string for trading pair {BTCUSD|ETHUSD}
    :arg size: int

    :returns: dict with min_ask/max_bid/dollar_value_min_asks/dollar_value_of_max_bids

    Notes
        Get Best Order Book Price
        GET /api/v3/ticker/bookTicker

    """
    url = ''.format(BINANCE_US_BASE_URL, symbol, size)
    pass


def get_binance_us_usd_trading_pairs():
    """Identifies all assets trading on Binance.US against US dollar.

    :returns: list of tickers

    Notes:
        https://docs.binance.us/#introduction
        https://api.binance.us/api/v3/ticker/price?symbol=BTCUSD
    """
    url = '{}/api/v3/exchangeInfo'.format(BINANCE_US_BASE_URL)
    resp = requests.get(url)
    resp_data = resp.json()
    symbols = resp_data.get('symbols')
    usd_assets = []

    for symbol in symbols:
        quote_asset = symbol.get('quoteAsset')
        base_asset = symbol.get('baseAsset')
        if quote_asset == 'USD' and base_asset in KNOWN_BINANCE_US_ASSETS:
            usd_assets.append(base_asset)
        elif quote_asset == 'USD':
            print('Unknown Binance.US USD trading pair encountered: {}'.format(base_asset))

    _ = check_for_delisting(KNOWN_BINANCE_US_ASSETS, usd_assets, 'Binance.US')
    return usd_assets


def get_coinbase_asset_price(symbol):
    """Identifies current asset price on Coinbase.
    :arg symbol: string for trading pair {BTC-USD|ETH-USD}

    :returns: dict with ask/bid/volume/price
    """
    url = '{}/products/{}/ticker'.format(COINBASE_BASE_URL, symbol)
    resp = requests.get(url)
    resp_data = resp.json()
    try:
        ask = float(resp_data.get('ask'))
        bid = float(resp_data.get('bid'))
        volume = float(resp_data.get('volume'))
        price = float(resp_data.get('price'))
    except TypeError:
        print('!!!!! Error in get_coinbase_asset_price for {}'.format(symbol))
        ask = bid = volume = price = None

    ret = {
        'ask': ask,
        'bid': bid,
        'volume': volume,
        'price': price,
    }
    return ret


def get_coinbase_order_book(symbol, size=5):
    """Retrieves details on Coinbase order book for a single asset.
    :arg symbol: string for trading pair {BTC-USD|ETH-USD}
    :arg size: int

    :returns: dict with min_ask/max_bid/dollar_value_min_asks/dollar_value_of_max_bids

    Notes:
        https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproductbook-1
    """
    url = '{}/products/{}/book?level=2'.format(COINBASE_BASE_URL, symbol)
    return get_order_book_helper(url, size)


def get_coinbase_usd_trading_pairs():
    """Identifies all assets trading on Coinbase against US dollar.

    :returns: list of tickers

    Notes:
        https://docs.cloud.coinbase.com/exchange/docs#get-historic-rates
        https://api.exchange.coinbase.com/products/{product_id}/ticker
    """
    url = '{}/products'.format(COINBASE_BASE_URL)
    resp = requests.get(url)
    data = resp.json()
    usd_assets = []
    for result in data:
        quote_currency = result.get('quote_currency')
        base_currency = result.get('base_currency')
        if quote_currency == 'USD' and base_currency in KNOWN_COINBASE_ASSETS:
            usd_assets.append(base_currency)
        elif quote_currency == 'USD':
            print('Unknown Coinbase trading pair encountered: {}'.format(base_currency))

    _ = check_for_delisting(KNOWN_COINBASE_ASSETS, usd_assets, 'Coinbase')
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


def get_kraken_asset_price(symbol):
    """Identifies current asset price on Kraken.
    :arg symbol: string for trading pair {BTCUSD|ETHUSD}

    :returns: dict with price/low/high/ask/bid
    """
    url = '{}/0/public/Ticker?pair={}'.format(KRAKEN_BASE_URL, symbol)
    resp = requests.get(url)
    data = resp.json()
    if data.get('error'):
        print('failed to get a successful response from {}/0/public/Ticker?pair={}'.format(KRAKEN_BASE_URL, symbol))
        return {}

    result = data.get('result', {})
    r_key = list(result.keys())[0]
    price_data = result.get(r_key)
    try:
        price = float(price_data.get('c')[0])
        low = float(price_data.get('l')[0])
        high = float(price_data.get('h')[0])
        ask = float(price_data.get('a')[0])
        bid = float(price_data.get('b')[0])
    except TypeError:
        print('!!!!! Error in get_kraken_asset_price for {}'.format(symbol))
        price = low = high = ask = bid = None

    ret = {
        'price': price,
        'low': low,
        'high': high,
        'ask': ask,
        'bid': bid,
    }
    return ret


def get_kraken_usd_trading_pairs():
    """Identifies all assets trading on Kraken against US dollar.

    :returns: list of tickers

    Notes:
        https://docs.kraken.com/rest/
        https://api.kraken.com/0/public/Ticker?pair=BTCUSD
    """
    url = '{}/0/public/AssetPairs'.format(KRAKEN_BASE_URL)
    resp = requests.get(url)
    data = resp.json()
    if data.get('error'):
        print('failed to get a successful response from https://api.kraken.com/0/public/AssetPairs')
        return []

    usd_assets = []
    results = data['result']
    for k, v in results.items():
        last_three = k[-3:]
        remove_last_three = k[:-3]
        if last_three == 'USD' and remove_last_three in KNOWN_KRAKEN_ASSETS:
            usd_assets.append(remove_last_three)
        elif last_three == 'USD':
            print('Unknown Kraken trading pair encountered: {}'.format(remove_last_three))

    _ = check_for_delisting(KNOWN_KRAKEN_ASSETS, usd_assets, 'Kraken')
    return usd_assets


def check_for_delisting(known_assets, discovered_assets, exchange_name):
    """Checks if a recent list of discovered assets contains something not in the known assets.
    :arg known_assets: list of tickers
    :arg discovered_assets: list of tickers
    :arg exchange_name: str

    :return: list of potentially delisted assets
    """
    asset_checker = collections.defaultdict(bool)
    missing_from_known_assets = []
    for known_asset in known_assets:
        asset_checker[known_asset] = True
    for discovered_asset in discovered_assets:
        if not asset_checker[discovered_asset]:
            print('{} was not identified on recent API call. Has {} delisted it?'.format(
                discovered_asset, exchange_name)
            )
            missing_from_known_assets.append(discovered_asset)

    return missing_from_known_assets


def get_order_book_helper(full_url, size=5, price_key='price', amount_key='amount'):
    """Retrieves details on order book for a single asset.
    :arg full_url: string
    :arg size: int
    :arg price_key: string
    :arg amount_key: string

    :returns: dict with min_ask/max_bid/dollar_value_min_asks/dollar_value_of_max_bids

    Notes:
        1. Response structure for full url can be a dictionary with a list of lists of bids/asks.
           The first item in a bid/ask should be the price and the second item should be a size.
        2. Response structure for full url can be a dictionary with a list of dicts of bid/asks.
           The bid/ask dict will have a price and amount key that can be supplied when the method
           is called.
    """
    def sum_bid_or_asks(item_list):
        sum_dollars = 0
        for i in range(min(len(item_list), size)):
            if type(item_list[i]) == list:
                sum_dollars += (float(item_list[i][0]) * float(item_list[i][1]))
            elif type(item_list[i]) == dict:
                sum_dollars += (float(item_list[i][price_key]) * float(item_list[i][amount_key]))
        return sum_dollars

    resp = requests.get(full_url)
    resp_data = resp.json()
    asks = resp_data.get('asks')
    bids = resp_data.get('bids')

    if type(asks[0]) == list:
        min_ask = asks[0][0]
    else:
        min_ask = asks[0][price_key]

    if type(bids[0]) == list:
        max_bid = bids[0][0]
    else:
        max_bid = bids[0][price_key]

    sum_asks = sum_bid_or_asks(asks)
    sum_bids = sum_bid_or_asks(bids)

    return {
        'min_ask': min_ask,
        'max_bid': max_bid,
        'dollar_value_min_asks': sum_asks,
        'dollar_value_max_bids': sum_bids,
    }
