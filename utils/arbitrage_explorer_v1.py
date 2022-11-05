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


TICKER_GROUP_SIZE = 5
WAIT_TIME_SECONDS = 30
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
                time.sleep(1)

        for ticker in small_ticker_group:
            print('----- {} -----'.format(ticker))
            print(asset_prices_by_ticker.get(ticker, 'Only available on 1 exchange'))

        # Wait before starting next ticker group to avoid hitting rate limits
        time.sleep(WAIT_TIME_SECONDS)


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
