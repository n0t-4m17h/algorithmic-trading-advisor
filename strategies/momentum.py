'''
This script will accept the value of your portfolio and tell you how many shares of the top 50 S&P 500
shares with the highest momentum from the past year, you should purchase.
'''

import pandas as pd
import requests
import math
from scipy.stats import percentileofscore as ptScore
import statistics

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
    # These are the data columns for each ticker ('Company Name' added to ease complexity of checks in the loop-ception)
    cols = [
        'Ticker', 
        'Company Name', 
        'Price', 
        'No. of Shares to Buy',
        '1-Year Price Return', 
        '1-Year Return Percentile',
        '6-Month Price Return',
        '6-Month Return Percentile',
        '3-Month Price Return',
        '3-Month Return Percentile',
        '1-Month Price Return',
        '1-Month Return Percentile',
        'HQM Score' # "High Quality Momentum"
    ]

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
        # since json response features each stock's quote, then concats each stock's stats, gotta double loop and check via company Name
        for ticker in data:
            # this outer loop will only apprehend the QUOTES dict, hence this try block 
            try:
                currCompanyName = str(ticker['companyName'])
                currSymbol = str(ticker['symbol'])
                currPrice = str(ticker['latestPrice'])
            except:
                continue # if this was a Stat dict
            # check if the ticker symbol has already been added, if so, then skip this stock (don't want to add duplicates)
            if (currCompanyName in completeDataFrame['Company Name'].unique()):
                continue
            # this inner loop will only apprehend the outer loop's STATS dict
            for ticker2 in data:
                # append each stock's info, of the current group, to the mega data frame
                if currCompanyName == str(ticker2['companyName']):
                    # Check if its the Quote dict or the Stat dict ('year1...' key will fail if former)
                    try:
                        newRow = pd.DataFrame([
                            currSymbol, 
                            currCompanyName, 
                            currPrice, 
                            'N/A',                              # No. of shares to buy
                            ticker2['year1ChangePercent'],      # 1-year price return
                            'N/A',                              # 1-year percentile
                            ticker2['month6ChangePercent'],     # 6-month price
                            'N/A',                              # 6-month percentile
                            ticker2['month3ChangePercent'],     # 3-month price
                            'N/A',                              # 3-month percentile
                            ticker2['month1ChangePercent'],     # 1-month price
                            'N/A',                              # 1-month percentile
                            'N/A'                               # HQM score
                        ], columns=[row], index=cols).T
                        completeDataFrame = pd.concat([completeDataFrame, newRow], ignore_index=True)
                        row += 1
                    except:
                        continue
        # break # stop at the first group

    # Loop thru and delete any rows where there is supposed to be a value from the api call.
    #       this'll prevent NoneType comparison issues later on 
    for row in completeDataFrame.index:
        if completeDataFrame.loc[row, '1-Year Price Return'] is None:
            completeDataFrame.drop(row, axis=0, inplace=True)
    
    return completeDataFrame



def calcPercentiles(dataFrame: pd.DataFrame):
    '''
        1. For each row in DF, loop thru each time period
        1.5. Get the Series/column of floats and use it with the specific entry's period value (who's pTile score we want to find)
             to calculate the percentile of that score, via scipy.stats' fnc
    '''
    global PERIODS; PERIODS = ['1-Year', '6-Month', '3-Month', '1-Month']

    for row in dataFrame.index:
        for epoch in PERIODS:
            # curr time period's price return array (the whole column of floats we're using to base our calculations on)
            epochsPriceReturn = dataFrame[f'{epoch} Price Return']
            # curr row's period's price return (an entry from that whole column who's percentile score we want to calculate)   
            rowsPriceReturn = dataFrame.loc[row, f'{epoch} Price Return']
            epochsPercentile = ptScore(epochsPriceReturn, rowsPriceReturn) / 100
            dataFrame.loc[row, f'{epoch} Return Percentile'] = epochsPercentile
    
    return dataFrame



def calcHQMscore(dataFrame: pd.DataFrame):
    '''
        HQM score is the arithmetic mean of all the percentile scores calculated just above. 
        1. For each entry in the DF, get the mean of all the "<X> Return Percentile" and add it to the "HQM" data column of the entry.
    '''
    for row in dataFrame.index:
        momentumPtile = []
        for epoch in PERIODS:
            momentumPtile.append(dataFrame.loc[row, f'{epoch} Return Percentile']) # is considered a string
            dataFrame.loc[row, 'HQM Score'] = statistics.mean(momentumPtile)
    return dataFrame



def filterLowMomentum(dataFrame: pd.DataFrame):
    '''
        1. Sort the dataframe by HQM score, descending order
        2. Remove all the stocks outside the top 50, which would be the "low momentum" stocks
    '''
    # Sort the DF in ascending order and alter the original variable
    dataFrame.sort_values('HQM Score', ascending=False, inplace=True)
    # list splice to keep only top 50
    dataFrame = dataFrame[:50]
    # Reset the row index and alter the original variable
    dataFrame.reset_index(drop=True, inplace=True)

    return dataFrame



def calcSharesToBuy(dataFrame: pd.DataFrame, portValue: float):
    '''
        Given your portfolio's value (how to calc it -> https://www.sapling.com/5872650/calculate-portfolio-value),
        use the established formula to find the number of shares to buy, per stock, if you want to make an
        equal-weight basket of those stocks. 
    '''
    posSize = portValue / len(dataFrame.index)
    # for each stock, the no. of shares to buy is the position size divided by the current market price
    for i in range(0, len(dataFrame.index)):
        # Calc the num of shares to buy of the current stock via each stock's price, and then assign the value to the empty column.
        #       (better to floor instead of ceiling, because you don't want to end up buying more than you can afford i.e. higher risk)
        numToBuy = math.floor(posSize / float(dataFrame.loc[i, 'Price']))
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
    percentFormat = workbook.add_format({'num_format': '0.0%'})

    worksheet.set_column('A:A', 9, tickerFormat)
    worksheet.set_column('B:B', 20, None)
    worksheet.set_column('C:C', 9, priceFormat)
    worksheet.set_column('D:D', 20, None)
    repLetters = ['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    # Same format from columns E to L
    for l in repLetters:
        worksheet.set_column(f'{l}:{l}', 20, percentFormat)
    worksheet.set_column('M:M', 10, percentFormat)

    xlWriter.close()



#########################
##### MAIN function #####
#########################
if __name__ == '__main__':
    try:
        print("Fetching mega dataframe of stock quotes and stats...", end=" ")
        dataFrame = initDataFrame()
        print("Acquired!\n")

        print("Calculating each stock's momentum percentiles...\n")
        dataFrame = calcPercentiles(dataFrame)

        print("Calculating each stock's HQM score...\n")
        dataFrame = calcHQMscore(dataFrame)

        print("Filtering out low momentum stocks...\n")
        dataFrame = filterLowMomentum(dataFrame)

        # initDataFrame() takes a long time, so keep this in a loop
        portfolioValue = 0.0
        while True:
            try: 
                portfolioValue = float(input("Enter the value of your portfolio:\n(aggregation of the value of each individual stock)\n>> "))
                break
            except ValueError as VE:
                print("Please enter a number!\n")
        print(f"Portfolio value '${portfolioValue}' recieved!\n")
        
        print("Calculating no. of shares to buy for each stock...\n")
        calcSharesToBuy(dataFrame, portfolioValue)
        
        print("Generating Excel file...\n")
        outputAsExcel(dataFrame)
        print("stonks 📈 !!")
    
    except Exception as e:
        print(f"ERROR: {e}")