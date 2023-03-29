import pandas as pd
from src import MyDirectories
import numpy as np
import scipy.stats as stats
import statsmodels.stats.diagnostic as diag
import matplotlib.pyplot as plt
import statsmodels.graphics.tsaplots as tsaplots


#read residuals from file
OUTPUT = MyDirectories.getTempDir() + "/output/"
my_dataframe = pd.read_csv(OUTPUT+'residual.csv')
residuals = my_dataframe.to_numpy().flatten()
print(residuals)

# Perform normality test using Q-Q plot
fig, ax = plt.subplots()
stats.probplot(residuals, plot=ax)
ax.set_title('Q-Q Plot of Residuals')
plt.show()

# Split the data into two subgroups based on the values of the independent variable
split_index = int(len(residuals) / 2)
resid_group1 = residuals[:split_index]
resid_group2 = residuals[split_index:]

# Perform the Goldfeld-Quandt test for homoscedasticity
fvalue, pvalue = stats.f_oneway(resid_group1**2, resid_group2**2)
print('Goldfeld-Quandt Test:')
print(f'F test statistic: {fvalue:.3f}')
print(f'F test p-value: {pvalue:.3f}')

# Perform independence test using autocorrelation plot
fig, ax = plt.subplots()
tsaplots.plot_acf(residuals, ax=ax, lags=np.arange(len(residuals)))
ax.set_title('Autocorrelation Plot of Residuals')
plt.show()
