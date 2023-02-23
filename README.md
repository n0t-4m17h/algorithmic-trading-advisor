# Algorithmic Trading Advisor
<!-- 3 simple python scripts that provides investment recommendations via the relative quantitative trading strategies. -->
A python bot that automates large data analysis to provide investment recommendations via 3 quantitative trading strategies.
<br/>

#### Requirements 📝
- ``` cd ``` into the main project directory and run ```pip3 install -r requirements.txt``` to install the required package versions. 
    - also, python 3.8.10 minimum is required.
- Must also create an account with IEX Cloud's [Apperate](https://iexcloud.io/cloud-login#/register) software, to gain access to the real-time data for free via an api token, but only for 30 days.
<br/>

### Program Execution 🐱‍💻
1. ```cd``` into main dir, then replace '*sp-500-tickers.csv*' with the csv file of your companies of interest (or just keep all of them).
2. Then run ```python3 strategies/<strat-of-your-choice>.py```, or run it via Jupyter Notebook (recommended)
<br/>

### Features / Investing Strategies 📈
*(in simple terms)*
- **Momentum trading:**
    - Investing in stocks that have increased in price the most. 
    - We quantitatively assess the price changes over the last 12 months, excluding the past month, and select the stock with the highest recent price return over the last year, as the most preferred investment.
- **Value trading:**
    - Investing in stocks that are trading below their true value, i.e. appears undervalued, relative to their business values, such as earnings. 
    - A concept called 'Multiples' is used to quantitatively estimate how valuable a company is.
        - P/E Ratio is a common example of a Multiple.  
    - "You must value the business in order to value the stock." ~ Charlie Munger.
- **Equal Weighted Index Fund:**
    - Most stock indexes are indexed via market capitalisation or price-weighted, where the index weighs / gives more importance to stocks to with either high market caps or as per their price. 
    - Building and Equal-Weight index will assign all stocks equal value and equal investment consideration. 
        - This means that if a stock in an index fund, has a price increase, shares will be sold in order to equally balance out the index fund, and vice versa. 

<br/>

### Known Issues 🤨
- some ticker's [rarely] info are lost during the API call, so their 'Market Cap', '{x} Price Return', etc. values would be empty in the output files. This has been apprehended, for now, by removing the whole stock entry from the data frame.

<br/>
### Possible Future Improvements 🤔
- Need to do some backtesting on historical data to quantify bot efficiency.
- Change API to [Alpha Vantage's](https://www.alphavantage.co/), as they supposedly provide free real-time data, and IEX Cloud's is only free for 30 days. 