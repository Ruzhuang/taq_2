import pandas as pd
import matplotlib.pyplot as plt
from src import MyDirectories
import numpy as np
import statistics
import ast
from scipy.optimize import curve_fit
from scipy.stats import norm


#daily value
def V(vwap_400,total_daily_volume):
    temp=vwap_400.multiply(total_daily_volume)
    rolling_mean = temp.rolling(window=10, min_periods=1).mean()
    # rolling_mean.fillna(value=temp[:10].mean(), inplace=True)
    return np.ravel(rolling_mean)

#temparory impact
def h(vwap_330, arrival_price, terminal_price):
    df_h=(vwap_330 - arrival_price) - (terminal_price-arrival_price)/2
    return np.ravel(df_h.values)


NUM_2_MINS = 195
def sigma(returns):
    copy=returns.copy()
    for i in range(returns.shape[0]):
        for j in range(returns.shape[1]):
            l=[]
            for x in range(max(0,i-9),i+1):
                l.extend(list(filter(None, ast.literal_eval(returns.iloc[x].iloc[j]))))
            copy.iloc[i].iloc[j]=statistics.stdev(l)*NUM_2_MINS
    return np.ravel(copy)

#daily imbalance
def X(vwap_400,imbalance):
    temp = vwap_400.multiply(imbalance)
    rolling_mean = temp.rolling(window=10, min_periods=1).mean()
    # rolling_mean.fillna(value=temp[:10].mean(), inplace=True)
    return np.ravel(rolling_mean)
def my_func(x, eta, beta):
    sigma, X, V=x
    return np.sign(X)*eta*sigma*np.power(abs(X)/((6/6.5)*V),beta)
def regress(sigma, X, V, h):

    # Fit the function to the data using curve_fit
    params, _ = curve_fit(my_func, [sigma,X,V], h, p0=[1, 2],bounds=([0,0],[100,10]))
    return params

np.random.seed(seed=10000)


if __name__ == "__main__":
    output_name="200_tickers_"
    OUTPUT = MyDirectories.getTempDir() + "/output/"
    _output_path = OUTPUT + output_name

    returns=pd.read_csv(_output_path + "returns.csv",index_col=0)
    total_daily_volume=pd.read_csv(_output_path + "total_daily_volume.csv",index_col=0)
    arrival_price=pd.read_csv(_output_path + "arrival_price.csv",index_col=0)
    terminal_price=pd.read_csv(_output_path + "terminal_price.csv",index_col=0)
    imbalance=pd.read_csv(_output_path + "imbalance.csv",index_col=0)
    vwap_330=pd.read_csv(_output_path + "vwap_330.csv",index_col=0)
    vwap_400=pd.read_csv(_output_path + "vwap_400.csv",index_col=0)
    print("finish reading...")


    #check for nan values, and drop them
    df_list=[returns,total_daily_volume,arrival_price,terminal_price,imbalance,vwap_330,vwap_400]
    drop_rows=[]
    for df in df_list:
        new_drop_rows = df[df.isna().sum(axis=1) >= 3].index.tolist()
        drop_rows.extend(new_drop_rows)
    for df in df_list:
        df.drop(index=drop_rows, inplace=True)
    print("Dropped rows:", drop_rows)

    dropped_cols=[]
    for df in df_list:
        # Drop columns that contain any None values
        new_dropped_cols = df.columns[df.isna().any()].tolist()
        dropped_cols.extend(new_dropped_cols)
    for df in df_list:
        df.drop(columns=dropped_cols, inplace=True)
    print("Dropped columns:", dropped_cols)

    #divide into two halfs according to volume
    # since we used heapq.nlargest() to form the no_nan_dates_and_largest_200_tickers...csv file, we
    # use the first half as the larger-stocks half and second the smaller
    def divide(df):
        num_cols = len(df.columns)
        midpoint = num_cols // 2
        left_df = df.iloc[:, :midpoint + 1]
        right_df = df.iloc[:, midpoint:]
        return left_df,right_df

    returns_left,returns_right = divide(returns)
    total_daily_volume_left, total_daily_volume_right = divide(total_daily_volume)
    arrival_price_left,arrival_price_right = divide(arrival_price)
    terminal_price_left, terminal_price_right = divide(terminal_price)
    imbalance_left, imbalance_right = divide(imbalance)
    vwap_330_left, vwap_330_right = divide(vwap_330)
    vwap_400_left, vwap_400_right = divide(vwap_400)

    X_left=X(vwap_400_left,imbalance_left)
    h_left=h(vwap_330_left, arrival_price_left, terminal_price_left)
    sigma_left=sigma(returns_left)
    V_left=V(vwap_400_left,total_daily_volume_left)
    eta_left, beta_left=regress(sigma_left,X_left,V_left,h_left)
    print("eta_left: ", eta_left)
    print("beta_left): ", beta_left)

    X_right=X(vwap_400_right,imbalance_right)
    h_right=h(vwap_330_right, arrival_price_right, terminal_price_right)
    sigma_right=sigma(returns_right)
    V_right=V(vwap_400_right,total_daily_volume_right)
    eta_right, beta_right=regress(sigma_right,X_right,V_right,h_right)
    print("eta_right: ",eta_right)
    print("beta_right: ", beta_right)

