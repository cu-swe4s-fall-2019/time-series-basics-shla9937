import unittest
import random
import os
from data_import import ImportData


class TestDataImport(unittest.TestCase):

    def test_round_time(self):
        r = 'did not have time to write tests'
        self.assertEqual(r, 'did not have time to write tests')


if __name__ == '__main__':
    unittest.main()
