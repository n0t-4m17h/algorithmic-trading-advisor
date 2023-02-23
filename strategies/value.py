'''
This script will accept the value of your portfolio and tell you how many shares of the top 50 S&P 500
shares with the highest estimated true value, you should purchase.
'''

import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math
from scipy.stats import percentileofscore as ptScore
import statistics

from secret import IEX_CLOUD_API_TOKEN

# NOTE: if running in Jupyter Notebook, concat "../" to the head (if not already there), else remove it
FILEPATH = '../sp-500-tickers.csv'
OUTPUTPATH = '../output/rec-value.xlsx'


##########################
##### CORE functions #####
##########################