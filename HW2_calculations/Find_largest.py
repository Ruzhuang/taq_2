import pandas as pd
import matplotlib.pyplot as plt
from src import MyDirectories
from src.FileManager import FileManager
import heapq

def Find_largest_volume_stocks(num_largest,startDateString="20070619",endDateString="20070921"):
    baseDir = MyDirectories.getTAQDir()
    sp500Path = baseDir + '/s&p500.xlsx'
    df_original = pd.read_excel(sp500Path, sheet_name='WRDS', usecols="H")

    df=df_original.copy()
    tickers=df['Ticker Symbol'].dropna().unique()

    #find the largest-volume stocks in sp500 from the 1st day's data
    fm = FileManager(baseDir)
    tradeDates = fm.getTradeDates(startDateString, endDateString)
    tradeDates.sort()

    volumes={ticker: 0 for ticker in tickers}
    for ticker in tickers:
        num=0
        for date in tradeDates:
            if(num==9):
                break
            try:
                file=fm.getTradesFile(date,ticker)
                volumes[ticker]+=file.getN()
                num+=1
            except Exception:
                continue
    largest_tickers = heapq.nlargest(num_largest, volumes, key=volumes.get)

    return largest_tickers

def drop_nan(largest_tickers,startDateString="20070619",endDateString="20070921"):
    baseDir = MyDirectories.getTAQDir()
    sp500Path = baseDir + '/s&p500.xlsx'
    # find the largest-volume stocks in sp500 from the 1st day's data
    fm = FileManager(baseDir)
    tradeDates = fm.getTradeDates(startDateString, endDateString)
    tradeDates.sort()
    df_2=pd.DataFrame(index=tradeDates,columns=largest_tickers)
    for ticker in largest_tickers:
        for date in tradeDates:
            try:
                trade_file=fm.getTradesFile(date,ticker)
                quote_file = fm.getQuotesFile(date, ticker)
                df_2.loc[date][ticker]=1
            except Exception:
                df_2.loc[date][ticker]=None

    print("original shape: ", df_2.shape)
    # Drop rows that contain at least 5 None values
    dropped_rows = df_2[df_2.isna().sum(axis=1) >= 5].index.tolist()
    df_2.drop(index=dropped_rows, inplace=True)
    print("Dropped rows:", dropped_rows)

    # Drop columns that contain any None values
    dropped_cols = df_2.columns[df_2.isna().any()].tolist()
    df_2.drop(columns=dropped_cols, inplace=True)
    print("Dropped columns:", dropped_cols)

    print("Check if there are any None value left: ",df_2.isna().any().any())
    print("shape after dropping: ", df_2.shape)

    df_2.values[:,:] = None

    OUTPUT = MyDirectories.getTempDir() + "/output"
    csv_path = OUTPUT + "/No_nan_dates_and_largest_{}_tickers_in_{}-{}.csv".format(len(largest_tickers), startDateString, endDateString)
    df_2.to_csv(csv_path)
    print("file saved to: ",csv_path)


if __name__ == '__main__':
    largest=Find_largest_volume_stocks(200)
    drop_nan(largest)

