from unittest.mock import patch
import unittest

# TODO Figure out how these imports work to not have to use sys.path.append
import sys
sys.path.append("...")  # Adds higher directory to python modules path.

from utils.exchange_apis import (
    convert_ticker_to_symbol,
    get_gemini_order_book,
    get_okcoin_order_book,
    get_binance_us_order_book,
    get_coinbase_order_book,
    get_kraken_order_book,
    get_order_book_helper,
)


class TestExchangeApisMethods(unittest.TestCase):

    def test_convert_ticker_to_symbol_binance_us(self):
        symbol = convert_ticker_to_symbol('BTC', 'binance.us')
        self.assertEqual(symbol, 'BTCUSD')

    def test_convert_ticker_to_symbol_coinbase(self):
        symbol = convert_ticker_to_symbol('BTC', 'coinbase')
        self.assertEqual(symbol, 'BTC-USD')

    def test_convert_ticker_to_symbol_gemini(self):
        symbol = convert_ticker_to_symbol('BTC', 'gemini')
        self.assertEqual(symbol, 'btcusd')

    def test_convert_ticker_to_symbol_kraken(self):
        symbol = convert_ticker_to_symbol('BTC', 'kraken')
        self.assertEqual(symbol, 'BTCUSD')

    def test_convert_ticker_to_symbol_okcoin(self):
        symbol = convert_ticker_to_symbol('BTC', 'okcoin')
        self.assertEqual(symbol, 'BTC-USD')

    @patch('requests.get')
    def test_get_gemini_order_book(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'bids': [{'price': '1.10', 'amount': '200'}, {'price': '1.08', 'amount': '200'}],
            'asks': [{'price': '1.50', 'amount': '200'}, {'price': '1.54', 'amount': '200'}],
        }
        order_book_data = get_gemini_order_book('btcusd')
        self.assertEqual(order_book_data.get('min_ask'), 1.50)
        self.assertEqual(order_book_data.get('max_bid'), 1.10)
        self.assertEqual(order_book_data.get('dollar_value_max_bids'), 436.00)
        self.assertEqual(order_book_data.get('dollar_value_min_asks'), 608.00)

    @patch('requests.get')
    def test_get_okcoin_order_book(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'bids': [['1.10', '200'], ['1.08', '200']],
            'asks': [['1.50', '200'], ['1.54', '200']],
        }
        order_book_data = get_okcoin_order_book('BTC-USD')
        self.assertEqual(order_book_data.get('min_ask'), 1.50)
        self.assertEqual(order_book_data.get('max_bid'), 1.10)
        self.assertEqual(order_book_data.get('dollar_value_max_bids'), 436.00)
        self.assertEqual(order_book_data.get('dollar_value_min_asks'), 608.00)

    def test_get_binance_us_order_book(self):
        # TODO
        self.assertTrue(True)

    def test_get_coinbase_order_book(self):
        # TODO
        self.assertTrue(True)

    def test_get_kraken_order_book(self):
        # TODO
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
