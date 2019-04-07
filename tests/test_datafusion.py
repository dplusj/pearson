from unittest import TestCase
from correlation.datafusion import DataFusion

class TestDataFusion(TestCase):
    def setUp(self):
        self.dataFusion = DataFusion('/tmp/datafusion', '331OE1QFUU07QNYL')

    def test_is_valid_codes(self):
        self.assertTrue(self.dataFusion.isValidCodes(['A', 'AAPL', 'MSFT']))
        self.assertFalse(self.dataFusion.isValidCodes(['FakeCode', 'AAPL', 'MSFT']))

