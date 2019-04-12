import os
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from datetime import datetime

METASTORE = 'metastore'
DATEFORMAT = '%Y-%m-%d'
HDFSTORE = 'store.h5'
DATAINDEX = 'date'


class DataFusion(object):
    """This class can query data remotely and sync with local cache
    """

    def __init__(self, dataPath, apiKey):
        """ Initialize the class
        Keyword Arguments:
            dataPath:  path to store the local data cache
            apiKey:  Alpha Vantage api key
        """
        self.ts = TimeSeries(key=apiKey, output_format='pandas')
        folder, filename = os.path.split(__file__)
        stockcodes = os.path.join(folder, "refdata", "USStockCode.csv")
        self.codeIndex = pd.read_csv(stockcodes)
        self.dataPath = dataPath
        if not os.path.exists(dataPath):
            print('creating new data folder: ' + dataPath)
            os.makedirs(dataPath)
        self.store = pd.HDFStore(self.dataPath+'/'+HDFSTORE)

    def query(self, code):
        """ query daily adjusted price data given the stock code
        Keyword Arguments:
            code:  stock symbol
        """
        querySize = 'full'
        refreshDate = self.getRefreshDate(code)
        today = datetime.now().date()
        if refreshDate is not None:
            if datetime.strptime(refreshDate, DATEFORMAT).date() < today:
                querySize = 'compact'
            else:
                return self.store[code]

        print('Fetching ' + code + ' data remotely...')
        data, meta_data = self.ts.get_daily_adjusted(
            symbol=code, outputsize=querySize)
        print('All data is loaded!')
        self.__save(code, data)
        return self.store[code]

    def getRefreshDate(self, code):
        """ Get the refresh date of requested stock, return None if not exist
        Keyword Arguments:
            code:  stock symbol
        """
        if METASTORE in self.store and code in self.store[METASTORE]:
            return self.store[METASTORE][code]
        else:
            return None

    def __save(self, code, data):
        """ save the data into local hdfstore and update the metastore
        Keyword Arguments:
            code:  stock symbol
            data:  pandas data frame which contains daily adjusted price data
        """
        if code in self.store:
            self.store[code] = \
                pd.concat([self.store[code], data]) \
                .reset_index() \
                .drop_duplicates(subset=DATAINDEX, keep='first') \
                .set_index(DATAINDEX)
        else:
            self.store[code] = data

        refreshDate = datetime.now().date().strftime(DATEFORMAT)
        metadata = pd.Series([refreshDate], index=[code])
        if METASTORE not in self.store:
            self.store[METASTORE] = metadata
        elif code in self.store[METASTORE]:
            metastore = self.store[METASTORE]
            metastore[code] = refreshDate
            self.store[METASTORE] = metastore
        else:
            self.store[METASTORE] = self.store[METASTORE].append(metadata)

    def isValidCodes(self, codes):
        """ check the validity of the input stock array,
        return false if any entry has invalid stock symbol
        Keyword Arguments:
            codes:  array of stock symbols
        """
        return pd.Series(codes).isin(self.codeIndex['USStockCode']).all()

    def exit(self):
        """ close the local hdfstore
        """
        self.store.close()
