'''
This script will accept the value of your portfolio and tell you how many shares of each S&P 500
constituent you should purchase to get an equal-weight version of the index fund.

S&P 500 market weights the TICKERS by market capitalisation, thus larger companies have a larger weight
in the index.
'''

import numpy as np # fast numerical computation
import pandas as pd # for tabular data, and dataframes (which hold tabular data)
import requests # for HTTP requests
import xlsxwriter # save Excel docs via python code
import math
# import yahooquery as yq
# import matplotlib.pyplot as plt
from secret import IEX_CLOUD_API_TOKEN


############################
##### HELPER functions #####
############################
def batchAPIchunks(alist, n):
    """ Yield successive n-sized chunks from lst."""
    for i in range(0, len(alist), n):
        yield alist[i:i + n]




##########################
##### CORE functions #####
##########################
def initDataFrame():
    '''
        1. Import the list of tickers
        2. Retrieve the free IEX Cloud API token (for authentication)
        3. Make the Batch API requests to [quickly] retrieve the necessary information
        4. Return the final data frame
    '''
    global TICKERS; TICKERS = pd.read_csv('sp-500-tickers.csv')
    # These are the data columns for each ticker
    cols = ['Ticker', 'Price', 'Market Capitalization', 'Number Of Shares to Buy']
    # Establish the above columns as the data sets basis
    completeDataFrame = pd.DataFrame(columns=cols)
    i = 0
    for ticker in TICKERS['Ticker']: # [:5]
        api_url = f'https://api.iex.cloud/v1/data/core/quote/{ticker}?token={IEX_CLOUD_API_TOKEN}'
        # Get the specific stock's information
        data = requests.get(api_url).json()[0]
        newRow = pd.DataFrame([ticker, data['latestPrice'], data['marketCap'], 'N/A'], columns=[i], index=cols).T # data['companyName']
        # append the current stock's row of info to the data set
        completeDataFrame = pd.concat([completeDataFrame, newRow], ignore_index=True)
        # print(completeDataFrame['Ticker'][i])
        i += 1
    return completeDataFrame


if __name__ == '__main__':
    dataFrame = initDataFrame()
    print(dataFrame)
