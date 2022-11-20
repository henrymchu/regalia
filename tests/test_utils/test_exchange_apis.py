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

    def test_convert_ticker_to_symbol(self):
        # TODO
        self.assertTrue(True)

    @patch('requests.get')
    def test_get_gemini_order_book(self, mock_get):
        # TODO
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'bids': [{'price': '1.10', 'amount': '2.0'}],
            'asks': [{'price': '1.50', 'amount': '2.0'}]
        }
        self.assertTrue(True)

    def test_get_okcoin_order_book(self):
        # TODO
        self.assertTrue(True)

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
