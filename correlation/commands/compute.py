from .base import Base
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns

DATEFORMAT = '%Y-%m-%d'
COLUMNDATE = 'date'
COLUMNSYMBOL = 'symbol'
COLUMNCLOSE = '5. adjusted close'

class Compute(Base):
    """Compute the correlation of stocks given the time window!"""

    def __init__(self, dataFusion, options, *args, **kwargs):
        super(Compute, self).__init__(options, args, kwargs)
        self.dataFusion = dataFusion

    def run(self):
        print('Computing correlation now...')
        print(self.options)
        startDate = self.__strToDateTime(self.options['--start-date'])
        lastDate = self.__strToDateTime(self.options['--last-date'])
        stocks = self.options['--stocks'].split(',')

        if startDate >= lastDate:
            raise ValueError("Failed: Input contains invalid time window")
        elif not self.dataFusion.isValidCodes(stocks):
            raise ValueError("Failed: Input has invalid stock codes: "+ self.options['--stocks'])

        symbols = []
        for s in stocks:
            data = self.__queryData(s, startDate, lastDate)
            if data is None:
                raise ValueError('Failed: No avaiable data of '+s+' given the time window')
            data[COLUMNSYMBOL] = s
            data[COLUMNCLOSE] = np.log(data[COLUMNCLOSE]).diff()
            data = data[1:]
            symbols.append(data)

        df = pd.concat(symbols)
        df = df.reset_index()
        df = df[[COLUMNDATE, COLUMNCLOSE, COLUMNSYMBOL]]
        df_pivot = df.pivot(COLUMNDATE, COLUMNSYMBOL, COLUMNCLOSE).reset_index()
        corr_df = df_pivot.corr(method='pearson')
        print('Correlation Table')
        print(corr_df)

        if self.options['--plot']:
            ax = sns.heatmap(corr_df.values, cmap="YlGnBu", xticklabels=corr_df.columns, yticklabels=corr_df.columns)
            plt.show()


    def __strToDateTime(self, date):
        return datetime.strptime(date, DATEFORMAT)

    def __dateTimeToStr(self, date):
        return date.strftime(DATEFORMAT)

    def __queryData(self, stock, sd, ld):
        data = self.dataFusion.query(stock)
        if sd >= self.__strToDateTime(data.index[0]) and ld <= self.__strToDateTime(data.index[-1]):
            return data[self.__dateTimeToStr(sd):self.__dateTimeToStr(ld)]
        else:
            return None



