'''
This script will 
'''
import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math
import scipy as sp

from secret import IEX_CLOUD_API_TOKEN

# NOTE: if running in Jupyter Notebook, concat "../" to the head (if not already there), else remove it
FILEPATH = '../sp-500-tickers.csv'
OUTPUTPATH = '../output/rec-momentum.xlsx'


##########################
##### CORE functions #####
##########################
def initDataFrame():
    '''
        1. Import the list of tickers
        2. Make the Batch API requests to retrieve stocks quote and stats
        3. Store into a dataframe and return it
    '''
    global TICKERS; TICKERS = pd.read_csv(FILEPATH)
    # These are the data columns for each ticker ('Company Name' added to ease complexity of checks in the loops)
    cols = ['Ticker', 'Company Name', 'Price', '1-yr Price Return', 'No. of Shares to Buy']

    tickersAsStrings = TICKERS['Ticker']
    # Establish the above columns as the data sets basis
    completeDataFrame = pd.DataFrame(columns=cols)
    step = 100
    # BATCH API METHOD: Make batch calls by groups of 100 stocks (API calls are total approx. 2mins ovrl, down from 8.5mins w/out batch calls)
    for i in range(0, len(tickersAsStrings), step):
        aTickerGroup = tickersAsStrings[i : i + step]
        tickGroupForCall = ','.join(aTickerGroup)
        # Get the current batch of stock's quote and stats
        batchAPIurl = f'https://api.iex.cloud/v1/data/core/quote,stats/{tickGroupForCall}?token={IEX_CLOUD_API_TOKEN}'
        data = requests.get(batchAPIurl).json()

        row = 0
        for ticker in data:
            # since json response features each stock's quote, then concats each stock's stats, gotta double loop and check via company Name
            # this outer loop will only apprehend the Quote dicts, hence this try block 
            try:
                currCompanyName = str(ticker['companyName'])
                currSymbol = str(ticker['symbol'])
                currPrice = str(ticker['latestPrice'])
            except:
                continue # if this was a Stat dict
            # check if the ticker symbol has already been added, if so, then skip this stock (don't want to add duplicates)
            if (currCompanyName in completeDataFrame['Company Name'].unique()):
                continue
            # this inner loop will only apprehend the outer loop's Stats dicts
            for ticker2 in data:
                # append each stock's info, of the current group, to the mega data frame
                if currCompanyName == str(ticker2['companyName']):
                    # Check if its the Quote dict or the Stat dict ('year1...' key will fail if former)
                    try:
                        newRow = pd.DataFrame([currSymbol, currCompanyName, currPrice, ticker2['year1ChangePercent'], 'N/A'], columns=[row], index=cols).T
                        completeDataFrame = pd.concat([completeDataFrame, newRow], ignore_index=True)
                        row += 1
                    except:
                        continue
        # break # stop at the first group
    return completeDataFrame



def outputAsExcel(dataFrame: pd.DataFrame):
    '''
        Given the completed dataFrame, output it into an excel file in a user-friendly fashion.
    '''
    xlWriter = pd.ExcelWriter(OUTPUTPATH, engine='xlsxwriter', )
    dataFrame.to_excel(xlWriter, sheet_name='Recommended Investments', index=False)

    workbook = xlWriter.book
    worksheet = xlWriter.sheets['Recommended Investments']
    
    # Set formatting per column
    tickerFormat = workbook.add_format({'bold': True})
    priceFormat = workbook.add_format({'num_format': '$0.00'})

    worksheet.set_column('A:A', 9, tickerFormat)
    worksheet.set_column('B:B', 18, None)
    worksheet.set_column('C:C', 9, priceFormat)
    worksheet.set_column('D:D', 18, None)
    worksheet.set_column('E:E', 18, None)

    xlWriter.close()


#########################
##### MAIN function #####
#########################
if __name__ == '__main__':
    # try:
    print("Fetching mega dataframe of stock quotes and stats...", end=" ")
    dataFrame = initDataFrame()
    print("Acquired!\n")

    print("\nGenerating Excel file...")
    outputAsExcel(dataFrame)
    print("\nstonks 📈 !!")
    
    # except Exception as e:
    #     print(f"ERROR: {e}")