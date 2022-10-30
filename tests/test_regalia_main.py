import unittest

# TODO Figure out how these imports work to not have to use sys.path.append
import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from regalia_main import validate_config


class TestRegaliaMainMethods(unittest.TestCase):
    good_config = {
        'exchanges': ['binance.us', 'coinbase'],
        'assets': ['BTC', 'ETH']
    }
    bad_config = {
        'exchanges': ['garbage', 'binance.us', 'coinbase'],
        'assets': ['BTC', 'ETH']
    }

    def test_validate_config_good_input(self):
        valid = validate_config(self.good_config)
        self.assertTrue(valid)

    def test_validate_config_bad_input(self):
        valid = validate_config(self.bad_config)
        self.assertFalse(valid)


if __name__ == '__main__':
    unittest.main()