from unittest import TestCase, mock
from correlation.datafusion import DataFusion
import uuid
import pandas as pd
import numpy as np
from datetime import datetime

class TestDataFusion(TestCase):
    def setUp(self):
        tempPath = '/tmp/df-' + str(uuid.uuid4()) 
        self.dataFusion = DataFusion(tempPath, '331OE1QFUU07QNYL')

    def tearDown(self):
        self.dataFusion.exit()

    def test_is_valid_codes(self):
        self.assertTrue(self.dataFusion.isValidCodes(['A', 'AAPL', 'MSFT']))
        self.assertFalse(self.dataFusion.isValidCodes(['FakeCode', 'AAPL', 'MSFT']))

    @mock.patch('alpha_vantage.timeseries.TimeSeries.get_daily_adjusted')
    def test_query(self, mockGet):
        df = pd.DataFrame(np.random.randn(10,2), columns=['a','b'])
        mockGet.return_value = (df, None)
        stock = 'xxx'
        self.assertEqual(self.dataFusion.getRefreshDate(stock), None)
        data = self.dataFusion.query(stock)
        self.assertEqual(data.shape[0], 10)
        self.assertEqual(data.shape[1], 2)
        self.assertEqual(self.dataFusion.getRefreshDate(stock), datetime.now().strftime('%Y-%m-%d'))
        self.dataFusion.query(stock)
        self.assertEqual(mockGet.call_count, 1)









