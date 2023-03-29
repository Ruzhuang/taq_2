# TAQ Project

**Team members**:  
Sihan Qi  sq543  
Sihan Liu sl6964  
Ruihan Zhuang rz1391  

## PDF
The PDF file for the answers to the questions are in TAQ2.pdf

## Dependency
Python version: 3.10
Pandas, numpy, matplotlib, gzip, statistics,
scipy, ast, statsmodels, unittest, _struct,
_collections, glob 

## Usage
All **implementation** files are in the HW2_calculations folder.

HW2_calculations:<br>
  -- Find_largest.py: Find the largest 200 stocks in s&p500, filter out the Nan values and save to No_nan_dates_and_largest_200_tickers_in_20070619-20070921.csv
The test of this file is in Test_Find_largest
<br>-- Reading_loop.py: Implement the reading loop. Output file will be in the output folder.
<br>-- Regression.py: perform regression on the stock data, and use bootstrap to find the p_value. The tests for both the regress function and the bootstrap function are in Test_Regression.py
<br> -- Regression_half.py: split the data into two halfs (larger stocks, smaller stocks) and compare the result of regression. The result is in the pdf.
<br> -- Residual_analysis.py: perform residual analysis for the residuals of regression. The results are in pdf.


All **unit test** files are in unit_test_2 folder. The _unit_test_ folder.


Change **MyDirectories.py** in src folder first, then **run** corresponding unit test file to run the project.


[//]: # ()
[//]: # (## Requirements: )

[//]: # (comment this out after finish writing)

[//]: # (1. README.txt file:)

[//]: # (&#40;a&#41; It should explain what parts of your code need to be changed to run your code in a different environment, including the installation of packages, references to databases and files, and assumptions about versions of Python and versions of packages used. To the extent possible, put references to absolute file locations and other constants as class variables in MyDirectories.py. &#40;An example of MyDirectories.py has been uploaded to your lecture content directory.&#41; Instructors and graders will have to be able to easiliy modify your MyDirectories.py to run your code in their environment.)

[//]: # (&#40;b&#41; It should explain how to run your unit tests.)

[//]: # (&#40;c&#41; Along with MyDirectories.py, it should specify where output files &#40;if any&#41; can be found.)
