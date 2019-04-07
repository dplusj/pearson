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
        self.ts = TimeSeries(key=apiKey, output_format='pandas')
        self.codeIndex = pd.read_csv('correlation/refdata/USStockCode.csv')
        self.dataPath = dataPath
        if not os.path.exists(dataPath):
            print('creating new data folder: ' + dataPath)
            os.makedirs(dataPath)
        self.store = pd.HDFStore(self.dataPath+'/'+HDFSTORE)

    def query(self, code):
        querySize = 'full'
        if METASTORE in self.store and code in self.store and code in self.store[METASTORE]:
            refreshDate = self.store[METASTORE][code]
            if datetime.strptime(refreshDate, DATEFORMAT).date() < datetime.now().date():
                querySize = 'compact'
            else:
                return self.store[code]

        print('Fetching '+ code +' data remotely...')
        data, meta_data = self.ts.get_daily_adjusted(symbol=code, outputsize=querySize)
        print('All data is loaded!')
        self.__save(code, data)
        return self.store[code]

    def __save(self, code, data):
        if code in self.store:
            self.store[code] = pd.concat([self.store[code], data]).reset_index().drop_duplicates(subset=DATAINDEX,
                                       keep='first').set_index(DATAINDEX)
        else: 
            self.store[code] = data

        refreshDate = datetime.now().date().strftime(DATEFORMAT)
        metadata = pd.Series([refreshDate], index=[code])
        if METASTORE not in self.store:
            self.store[METASTORE] = metadata
        elif code in self.store[METASTORE]:
            self.store[METASTORE][code] = refreshDate
        else:
            self.store[METASTORE] = self.store[METASTORE].append(metadata)

    def isValidCodes(self, codes):
        return pd.Series(codes).isin(self.codeIndex['USStockCode']).all()

    def exit(self):
        self.store.close()




