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
def chunks(alist, n):
    '''
    Yield successive n-sized chunks from a list
    (i.e. breakup a list into groups of size n)
    '''
    for i in range(0, len(alist), n):
        yield alist[i:i + n]




##########################
##### CORE functions #####
##########################
def initDataFrame():
    '''
        1. Import the list of tickers
        2. Make the Batch API requests to [quickly] retrieve the necessary information
        3. Return the final data frame
    '''
    global TICKERS; TICKERS = pd.read_csv('sp-500-tickers.csv')
    # These are the data columns for each ticker
    cols = ['Ticker', 'Price', 'Market Capitalization', 'Number Of Shares to Buy']

    tickersAsStrings = TICKERS['Ticker']
    # Establish the above columns as the data sets basis
    completeDataFrame = pd.DataFrame(columns=cols)
    step = 100
    # BATCH API METHOD: Make batch calls by groups of 100 stocks (API calls are approx. 40secs/group == approx. 3mins ovrl)
    for i in range(0, len(tickersAsStrings), step):
        aTickerGroup = tickersAsStrings[i : i + step]
        tickGroupForCall = ','.join(aTickerGroup)
        # Get the current batch of stock's informatio
        batchAPIurl = f'https://api.iex.cloud/v1/data/core/quote/{tickGroupForCall}?token={IEX_CLOUD_API_TOKEN}'
        data = requests.get(batchAPIurl).json()
        # print(data[0]['symbol']) # print first stock of each group
        row = 0
        for ticker in data:
            # append each stock's info, of the current group, to the mega data frame
            newRow = pd.DataFrame([ticker['symbol'], ticker['latestPrice'], ticker['marketCap'], 'N/A'], columns=[row], index=cols).T # data['companyName']
            completeDataFrame = pd.concat([completeDataFrame, newRow], ignore_index=True)
            row += 1

    return completeDataFrame


def howManySharesToBuy(dataFrame: pd.DataFrame, size: int):
    '''
        1.
    '''
    pass



if __name__ == '__main__':
    try:
        dataFrame = initDataFrame()
        print("Mega dataframe of stocks acquired")
        
        portfolioValue = int(input("Enter the value of your portfolio:\n>> "))
        howManySharesToBuy(dataFrame, portfolioValue)

    except Exception as e:
        print(f"ERROR: {e}")