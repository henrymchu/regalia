import unittest

# TODO Figure out how these imports work to not have to use sys.path.append
import sys
sys.path.append("...")  # Adds higher directory to python modules path.

from utils.arbitrage_explorer_v1 import segment_groups_of_n


class TestArbitrageExplorerV1Methods(unittest.TestCase):

    def test_segment_groups_of_n(self):
        # TODO
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()