# Identifies potential arbitrages for specific exchanges for specific assets

# Python imports
import collections
import math
import time

# TODO Figure out how these imports work to not have to use sys.path.append
import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from constants import (
    BINANCE_US_ID,
    COINBASE_ID,
    FTX_US_ID,
    GEMINI_ID,
    KRAKEN_ID,
    OKCOIN_ID,
)

# Local imports
from exchange_apis import (
    get_binance_us_usd_trading_pairs,
    get_coinbase_usd_trading_pairs,
    get_ftx_us_usd_trading_pairs,
    get_gemini_usd_trading_pairs,
    get_kraken_usd_trading_pairs,
    get_okcoin_usd_trading_pairs,
    get_asset_price_at_exchange,
)


TICKER_GROUP_SIZE = 10
WAIT_TIME_SECONDS = 11
EXCHANGE_IDS = [BINANCE_US_ID, COINBASE_ID, FTX_US_ID, GEMINI_ID, KRAKEN_ID, OKCOIN_ID]


def discover():
    tickers, availability = get_unique_tickers_and_availability_matrix()
    small_ticker_groups = segment_groups_of_n(tickers, TICKER_GROUP_SIZE)
    asset_prices_by_ticker = {}

    # Loop over the groups of tickers
    for small_ticker_group in small_ticker_groups:

        # Loop over each ticker in a group
        for ticker in small_ticker_group:
            single_asset_prices = []

            # If an asset if only available on one exchange, there's no reason to look for arbitrage
            sum_of_availability = availability[BINANCE_US_ID].get(ticker, 0) + \
                availability[COINBASE_ID].get(ticker, 0) + \
                availability[FTX_US_ID].get(ticker, 0) + \
                availability[GEMINI_ID].get(ticker, 0) + \
                availability[KRAKEN_ID].get(ticker, 0) + \
                availability[OKCOIN_ID].get(ticker, 0)

            if sum_of_availability > 1:
                # Loop over all exchanges for a single ticker
                for exchange_id in EXCHANGE_IDS:
                    if availability[exchange_id].get(ticker):
                        price = get_asset_price_at_exchange(ticker, exchange_id)
                        single_asset_prices.append((exchange_id, price))

                # Add list of prices for a single asset into map keyed by ticker
                asset_prices_by_ticker[ticker] = single_asset_prices
                info = get_price_delta(single_asset_prices)
                if info['percentage_delta']:
                    print('{}: delta: {}% - {} {} - {} {}'.format(
                        ticker,
                        round(info['percentage_delta'], 3),
                        info['low'],
                        info['cheap_exchange'],
                        info['high'],
                        info['expensive_exchange']
                    ))

        for ticker in small_ticker_group:
            print('----- {} -----'.format(ticker))
            print(asset_prices_by_ticker.get(ticker, 'Only available on 1 exchange'))

        # Wait before starting next ticker group to avoid hitting rate limits
        time.sleep(WAIT_TIME_SECONDS)

    # Go through asset prices by ticker and look for price deltas
    asset_price_delta_as_percentage_of_min_price = {}
    for ticker in asset_prices_by_ticker.keys():
        delta_info = get_price_delta(asset_prices_by_ticker[ticker])
        asset_price_delta_as_percentage_of_min_price[ticker] = {
            'percentage_delta': delta_info['percentage_delta'],
            'low': delta_info['low'],
            'cheap_exchange': delta_info['cheap_exchange'],
            'high': delta_info['high'],
            'expensive_exchange': delta_info['expensive_exchange'],
        }

    for ticker in asset_price_delta_as_percentage_of_min_price.keys():
        info = asset_price_delta_as_percentage_of_min_price[ticker]
        if info['percentage_delta']:
            print('{}: percentage: {}% - min: {} {} - max: {} {}'.format(
                ticker,
                round(info['percentage_delta'], 3),
                info['low'],
                info['cheap_exchange'],
                info['high'],
                info['expensive_exchange'],
            ))

    print('----- Greater than 4.5% deltas -----')
    for ticker in asset_price_delta_as_percentage_of_min_price.keys():
        info = asset_price_delta_as_percentage_of_min_price[ticker]
        pdelta = info['percentage_delta']
        if pdelta and pdelta >= 4.5:
            print('{}: percentage: {}% - min: {} {} - max: {} {}'.format(
                ticker,
                round(info['percentage_delta'], 3),
                info['low'],
                info['cheap_exchange'],
                info['high'],
                info['expensive_exchange'],
            ))


def get_unique_tickers_and_availability_matrix():
    """Creates a list of unique tickers and availability matrix for specific exchanges of interest.

    :returns: unique_tickers_list: list
              availability_matrix: defaultdict
    """
    unique_tickers = set()
    availability_matrix = collections.defaultdict(dict)
    for asset in get_binance_us_usd_trading_pairs():
        unique_tickers.add(asset)
        availability_matrix[BINANCE_US_ID][asset] = 1
    for asset in get_coinbase_usd_trading_pairs():
        unique_tickers.add(asset)
        availability_matrix[COINBASE_ID][asset] = 1
    for asset in get_ftx_us_usd_trading_pairs():
        unique_tickers.add(asset)
        availability_matrix[FTX_US_ID][asset] = 1
    for asset in get_gemini_usd_trading_pairs():
        unique_tickers.add(asset)
        availability_matrix[GEMINI_ID][asset] = 1
    for asset in get_kraken_usd_trading_pairs():
        unique_tickers.add(asset)
        availability_matrix[KRAKEN_ID][asset] = 1
    for asset in get_okcoin_usd_trading_pairs():
        unique_tickers.add(asset)
        availability_matrix[OKCOIN_ID][asset] = 1

    unique_tickers_list = list(unique_tickers)
    unique_tickers_list.sort()
    return unique_tickers_list, availability_matrix


def segment_groups_of_n(input_tickers, group_size=15):
    """Creates groups of n tickers.
    :arg: input_tickers: list
    :arg: group_size: int

    :returns: list of lists
    """
    segmented_groups = []
    number_of_groups = math.ceil(len(input_tickers) / group_size)
    for i in range(number_of_groups):
        starting_index = i * group_size
        ending_index = starting_index + group_size
        chunk_of_tickers = input_tickers[starting_index:ending_index]
        segmented_groups.append(chunk_of_tickers)
    return segmented_groups


def get_price_delta(asset_prices):
    """Identifies price delta as a percentage of the smallest price.
    :arg: asset_prices: list of tuples; each tuple's first item is an exchange identifier and second item is a price

    :returns: percentage_delta: float
              cheap_price: float
              cheap_exchange: str
              expensive_price: float
              expensive_exchange: str
    """
    prices = []
    for i in range(len(asset_prices)):
        if asset_prices[1]:
            prices.append(asset_prices[i])
    try:
        prices.sort(key=lambda x: x[1])
    except TypeError:
        print('error in get_prices_delta - possible comparison with float and None')
        return {
            'percentage_delta': None,
            'low': None,
            'cheap_exchange': None,
            'high': None,
            'expensive_exchange': None,
        }

    cheap = prices[0][1]
    expensive = prices[-1][1]
    percentage_delta = (expensive - cheap) / cheap * 100.0
    cheap_exchange = prices[0][0]
    expensive_exchange = prices[-1][0]

    return {
        'percentage_delta': percentage_delta,
        'low': cheap,
        'cheap_exchange': cheap_exchange,
        'high': expensive,
        'expensive_exchange': expensive_exchange,
    }
