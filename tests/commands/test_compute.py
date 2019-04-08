"""Tests for our compute-correlation command."""

from unittest import TestCase, mock
from correlation.commands.compute import Compute

class TestCompute(TestCase):
    def test_invalid_data_input(self):
        options = {
            '--start-date' : '2018-08-08',
            '--last-date' : '2017-07-07',
            '--stocks' : 'MSFT,GOOG'
        }

        with mock.patch('correlation.datafusion.DataFusion') as mocked_datafusion:
            with self.assertRaises(ValueError): 
                compute = Compute(mocked_datafusion, options)
                compute.run()

    def test_invalid_stocks_input(self):
        options = {
            '--start-date' : '2018-08-08',
            '--last-date' : '2019-07-07',
            '--stocks' : 'MSFT,FAKESTOCK'
        }

        with mock.patch('correlation.datafusion.DataFusion') as mocked_datafusion:
            with self.assertRaises(ValueError): 
                mocked_datafusion.isValidCodes.return_value = False
                compute = Compute(mocked_datafusion, options)
                compute.run()

        