'''
This script will accept the value of your portfolio and tell you how many shares of each S&P 500
constituent you should purchase to get an equal-weight version of the index fund.
'''

import pandas as pd
import requests
import math
# import yahooquery as yq
# import matplotlib.pyplot as plt
from secret import IEX_CLOUD_API_TOKEN



# NOTE: if running in Jupiter Notebook, concat "../" to the head, else remove it
FILEPATH = '../sp-500-tickers.csv'
OUTPUTPATH = '../output/rec-equal-weight.xlsx'

##########################
##### CORE functions #####
##########################
def initDataFrame():
    '''
        1. Import the list of tickers
        2. Make the Batch API requests to [quickly] retrieve the necessary information
        3. Store into a dataframe and return it
    '''
    global TICKERS; TICKERS = pd.read_csv(FILEPATH)
    # These are the data columns for each ticker
    cols = ['Ticker', 'Price', 'Market Cap', 'No. of Shares to Buy']

    tickersAsStrings = TICKERS['Ticker']
    # Establish the above columns as the data sets basis
    completeDataFrame = pd.DataFrame(columns=cols)
    step = 100
    # BATCH API METHOD: Make batch calls by groups of 100 stocks (API calls are total approx. 2mins ovrl, down from 8.5mins w/out batch calls)
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
        # break
    return completeDataFrame



def calcSharesToBuy(dataFrame: pd.DataFrame, portValue: float):
    '''
        Given the portfolio's value (how to calc it -> https://www.sapling.com/5872650/calculate-portfolio-value),
        use the established formula to find the number of shares to buy, per stock. 
    '''
    # Since this is an equal-weight index, each investment will have the same "position size", which
    #       will determine how much you should invest in the stock. 
    posSize = portValue / len(dataFrame.index)
    # for each stock, the no. of shares to buy is the position size divided by the current market price
    for i in range(0, len(dataFrame.index)):
        # Calc the num of shares to buy of the current stock via each stock's price, and then assign the value to the empty column.
        #       (better to floor instead of ceiling, because you don't want to end up buying more than you can afford i.e. higher risk)
        numToBuy = math.floor(posSize / dataFrame.loc[i, 'Price'])
        dataFrame.loc[i, 'No. of Shares to Buy'] = numToBuy



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
    mrktCapFormat = workbook.add_format({'num_format': '$#,##0'})

    worksheet.set_column('A:A', 9, tickerFormat)
    worksheet.set_column('B:B', 9, priceFormat)
    worksheet.set_column('C:C', 18, mrktCapFormat)
    worksheet.set_column('D:D', 18, None)

    xlWriter.close()



#########################
##### MAIN function #####
#########################
if __name__ == '__main__':
    try:
        print("Fetching mega dataframe of stock quotes...", end=" ")
        dataFrame = initDataFrame()
        print("Acquired!\n")

        # initDataFrame() takes a long time, so keep this in a loop
        portfolioValue = 0.0
        while True:
            try: 
                portfolioValue = float(input("Enter the value of your portfolio:\n(aggregation of the value of each individual stock)\n>> "))
                break
            except ValueError as VE:
                print("Please enter a number!\n")
        print(f"Portfolio value '${portfolioValue}' recieved!")
        calcSharesToBuy(dataFrame, portfolioValue)

        print("\nGenerating Excel file...")
        outputAsExcel(dataFrame)
        print("\nstonks 📈 !!")

    except Exception as e:
        print(f"ERROR: {e}")