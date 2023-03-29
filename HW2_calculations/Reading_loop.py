import pandas as pd
from src import MyDirectories
from src.FileManager import FileManager
from impactUtils.ReturnBuckets import ReturnBuckets
from impactUtils.TickTest import TickTest
from impactUtils.VWAP import VWAP


class Mid_quotes:
    def __init__(self, file):
        self._file = file

    def getPrice(self, i):
        return (self._file.getAskPrice(i) + self._file.getBidPrice(i)) / 2.0

    def getTimestamp(self, i):
        return self._file.getMillisFromMidn(i)

    def getN(self):
        return self._file.getN()
class Reading_loop:
    def __init__(self,file_name,output_name):
        self._file_name=file_name

        OUTPUT=MyDirectories.getTempDir()+"/output/"
        csv_path=OUTPUT+file_name
        self._output_path=OUTPUT+output_name

        self._df=pd.read_csv(csv_path, index_col=0)
        self._df.index = self._df.index.astype(str)

        self._dates=self._df.index
        self._tickers=self._df.columns


    '''
    For every stock in our list
        For every day of data
            Compute 2-minute mid-quote returns
            Compute total daily volume
            Compute arrival price – Average of first five mid-quote prices
            Compute imbalance between 9:30 and 3:30
            Compute volume-weighted average price between 9:30 and 3:30
            Compute volume-weighted average price between 9:30 and 4:00 (This will
            be used to compute average daily value of imbalance as described later in
            this document.)
            Compute terminal price at 4:00 – Average of last five mid-quote prices
    '''

    def reading_loop(self):
        # Instantiate a file manager
        baseDir = MyDirectories.getTAQDir()
        fm = FileManager(baseDir)
        NUM_2_MINS=195

        # matrices
        returns=self._df.copy().astype('object')
        total_daily_volume=self._df.copy()
        arrival_price=self._df.copy()
        imbalance=self._df.copy()
        vwap_330=self._df.copy()
        vwap_400=self._df.copy()
        terminal_price=self._df.copy()


        for date in self._dates:
            print(date)
            for ticker in self._tickers:
                trades=fm.getTradesFile(date,ticker)
                quotes=fm.getQuotesFile(date,ticker)
                mid_quotes = Mid_quotes(quotes)

                # Compute 2-minute mid-quote returns
                returnBuckets=ReturnBuckets(mid_quotes,None,None,NUM_2_MINS)
                returns.loc[date][ticker]=returnBuckets._returns

                # Compute total daily volume
                total_daily_volume.loc[date][ticker]=sum(trades._s)

                # Compute arrival price – Average of first five mid-quote prices
                arrival_price.loc[date][ticker]=sum([mid_quotes.getPrice(i) for i in range(5)])/5
                # Compute terminal price at 4:00 – Average of last five mid-quote prices
                last5=range(mid_quotes.getN()-5,mid_quotes.getN())
                terminal_price.loc[date][ticker]=sum([mid_quotes.getPrice(i) for i in last5])/5

                # Compute imbalance between 9:30 and 3:30
                tickTest = TickTest()
                start = 18 * 60 * 60 * 1000 / 2
                end330 = start + (6 * 60 * 60 * 1000)
                classifications = tickTest.classifyAll(trades, start, end330)
                # I modified the return value of tickTest.classifyAll so that it returns:
                # (data.getTimestamp(i), data.getPrice(i), self.classify(data.getPrice(i)), data.getSize(i))
                imbalance.loc[date][ticker]=sum([tup[3] * tup[2] for tup in classifications])

                # Compute volume-weighted average price between 9:30 and 3:30
                vwap = VWAP(trades, start, end330)
                vwap_330.loc[date][ticker] = vwap.getVWAP()
                # Compute volume-weighted average price between 9:30 and 4:00
                end4 = 16 * 60 * 60 * 1000
                vwap = VWAP(trades, start, end4)
                vwap_400.loc[date][ticker]=vwap.getVWAP()


        # matrices to csv
        returns.to_csv(self._output_path+"returns.csv")
        total_daily_volume.to_csv(self._output_path+"total_daily_volume.csv")
        arrival_price.to_csv(self._output_path+"arrival_price.csv")
        terminal_price.to_csv(self._output_path+"terminal_price.csv")
        imbalance.to_csv(self._output_path+"imbalance.csv")
        vwap_330.to_csv(self._output_path + "vwap_330.csv")
        vwap_400.to_csv(self._output_path + "vwap_400.csv")

if __name__ == "__main__":
    Reading_loop("No_nan_dates_and_largest_200_tickers_in_20070619-20070921.csv","200_tickers_").reading_loop()