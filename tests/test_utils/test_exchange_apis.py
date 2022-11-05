import unittest

# TODO Figure out how these imports work to not have to use sys.path.append
import sys
sys.path.append("...")  # Adds higher directory to python modules path.

from utils.exchange_apis import convert_ticker_to_symbol


class TestExchangeApisMethods(unittest.TestCase):

    def test_convert_ticker_to_symbol(self):
        # TODO
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()