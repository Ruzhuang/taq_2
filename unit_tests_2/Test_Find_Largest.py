from HW2_calculations.Find_largest import Find_largest_volume_stocks,drop_nan
import pandas as pd
import matplotlib.pyplot as plt
from src import MyDirectories

#this function call will print out the process of finding the stocks with
#largest volumes, the process of dropping "None"s and the remaining stock and
#dates would be in a csv file in output folder


real_largest=Find_largest_volume_stocks(20,"20070828","20070830")
print("real_largest 20 stocks: ",real_largest)

#make up the stocks with largest volumes to show the dropping process
fake_largest=['AAPL','XOM','SUNW']
drop_nan(fake_largest,"20070828","20070830")
