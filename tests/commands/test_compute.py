"""Tests for our compute-correlation command."""

from unittest import TestCase, mock
from correlation.commands.compute import Compute
import pandas as pd
import numpy as np

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

    def test_compute_correlation(self):
        options = {
            '--start-date' : '2018-08-08',
            '--last-date' : '2018-08-10',
            '--stocks' : 'MSFT,FB'
        }

        with mock.patch('correlation.datafusion.DataFusion') as mocked_datafusion:
            mocked_datafusion.isValidCodes.return_value = True
            d = {'date': ['2018-08-08', '2018-08-09', '2018-08-10'], '5. adjusted close': [1, 2, 3]}
            df = pd.DataFrame(d)
            df = df.set_index('date')
            mocked_datafusion.query.return_value = df
            compute = Compute(mocked_datafusion, options)
            corr_df = compute.run()
            self.assertEqual(corr_df.iloc[1,0], 1)
            self.assertEqual(corr_df.iloc[0,1], 1)


        