# Algorithmic Trading Advisor
<!-- 3 simple python scripts that provides investment recommendations via the relative quantitative trading strategies. -->
A python bot that automates large data analysis to provide investment recommendations via 3 quantitative trading strategies.
<br/>

**Requirements**
- ``` cd ``` into the main project directory and run ```pip install -r requirements.txt``` to install the required package versions. 
    - also, python 3.8.10 minimum is required.
- Must also create an account with IEX Cloud's [Apperate](https://iexcloud.io/cloud-login#/register) software, to gain access to the real-time data for free, but only for 30 days *(NOTE: [Alpha Vantage](https://www.alphavantage.co/) supposedly provides free real-time data via their API, which is worth looking into)*. 
<br/>

### Execution
1. ```cd``` into main dir, then replace '*sp-500-tickers.csv*' with the csv file of your companies of interest (or just keep all of them).
2. Then run ```python3 strategies/<strat-of-your-choice>.py```, or run it via Jupyter Notebook (recommended)
<br/>

### Features / Investing Strategies 
*(in simple terms)*
- **Momentum trading:**
    - Investing in stocks that have increased in price the most. 
    - We assess the price changes over the last 12 months, excluding the past month, and select the stock with the highest recent price return over the last year, as the preferred investment.
- **Value trading:**
    - Investing in stocks that are trading below their true value, i.e. appears undervalued, relative to their business values, such as earnings. 
    - A concept called 'Multiples' is used to estimate how valuable a company is.
        - P/E Ratio is a common example of a Multiple.  
    - "You must value the business in order to value the stock." ~ Charlie Munger.
- **Equal Weighted Index Fund:**
    - Most stock indexes are indexed via market capitalisation or price-weighted, where the index weighs / gives more importance to stocks to with either high market caps or as per their price. 
    - Building and Equal-Weight index will assign all stocks equal value and equal investment consideration. 
        - This means that if a stock in an index fund, has a price increase, shares will be sold in order to equally balance out the index fund, and vice versa. 

<br/>

### Known Issues
- some tickers [rarely] are lost during the API call, so their 'Market Cap', '1-yr Price Return' value would be empty in the output files, or maybe even the whole row of info.

### Possible Future Improvements
- Need to do some backtesting on historical data.