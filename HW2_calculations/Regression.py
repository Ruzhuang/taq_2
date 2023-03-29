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

np.random.seed(seed=0)
def residual_bootstrap(sigma, X, V, h, beta, eta):
    print("original eta: ", eta)
    print("original beta: ", beta)
    residual= h-my_func((sigma, X, V),eta,beta)
    m=10
    beta_list=[]
    eta_list=[]
    for i in range(m):
        new_residual = np.random.choice(residual, size=len(residual), replace=True)
        new_h=my_func((sigma, X, V),eta,beta)+new_residual
        new_eta, new_beta=regress(sigma,X,V,new_h)

        beta_list.append(new_beta)
        eta_list.append(new_eta)
    print("list of new eta: ", eta_list)
    print("list of new beta: ", beta_list)
    se_beta=statistics.stdev(beta_list)
    t_stat_beta=(beta-0)/se_beta
    print("t_stat_beta: ", t_stat_beta)
    se_eta = statistics.stdev(eta_list)
    t_stat_eta = (eta - 0) / se_eta
    print("t_stat_eta: ", t_stat_eta)
    return norm.sf(np.abs(t_stat_eta)) * 2, norm.sf(np.abs(t_stat_beta)) * 2

def pair_bootstrap(sigma, X, V, h, beta, eta):
    m=10
    beta_list=[]
    eta_list=[]
    for i in range(m):
        new_index = np.random.choice(range(len(sigma)), size=len(sigma), replace=True)
        new_sigma=np.take(sigma, new_index)
        new_X=np.take(X, new_index)
        new_V=np.take(V, new_index)
        new_h=np.take(h, new_index)
        new_eta, new_beta=regress(new_sigma,new_X,new_V,new_h)
        beta_list.append(new_beta)
        eta_list.append(new_eta)
    print("original eta: ", eta)
    print("original beta: ", beta)
    print("list of new eta: ", eta_list)
    print("list of new beta: ", beta_list)
    se_beta=statistics.stdev(beta_list)
    t_stat_beta=(beta-0)/se_beta
    print("t_stat_beta: ", t_stat_beta)
    se_eta = statistics.stdev(eta_list)
    t_stat_eta = (eta - 0) / se_eta
    print("t_stat_eta: ", t_stat_eta)
    return norm.sf(np.abs(t_stat_eta)) * 2, norm.sf(np.abs(t_stat_beta)) * 2


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

    X=X(vwap_400,imbalance)
    h=h(vwap_330, arrival_price, terminal_price)
    sigma=sigma(returns)
    V=V(vwap_400,total_daily_volume)
    eta, beta=regress(sigma,X,V,h)
    print("eta: ",eta)
    print("beta: ", beta)
    p_value_eta, p_value_beta=residual_bootstrap(sigma, X, V, h, beta, eta)
    print("residual bootstrap:")
    print("p_value_eta: ", p_value_eta)
    print("p_value_beta: ", p_value_beta)
    p_value_eta, p_value_beta=pair_bootstrap(sigma, X, V, h, beta, eta)
    print("pair bootstrap:")
    print("p_value_eta: ", p_value_eta)
    print("p_value_beta: ", p_value_beta)
    residual=h-my_func((sigma, X, V),eta,beta)

    #store the residuals to a file
    my_series = pd.Series(residual)
    my_series.to_csv(OUTPUT+'residual_1.csv', index=False)
