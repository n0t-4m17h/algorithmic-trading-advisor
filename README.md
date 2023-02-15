# Algorithmic Trading Bot
A simple Python bot that provides investment recommendations via quantitative trading strategies. 
<br/>

**Requirements**
- ``` cd ``` into the main directory and run ```pip install -r requirements.txt``` to install the required package versions. 
- Must also create an account with IEX Cloud's [Apperate](https://iexcloud.io/cloud-login#/register) software, to gain access to the real-time data for free, but only for 30 days *([Alpha Vintage](https://www.alphavantage.co/) supposedly provides free real-time data via their API, which is worth looking into)*. 
<br/>

### Features / Investing Strategies 
*(in simple terms)*
- Equal Weighted [S&P/ASX] Index Fund:
    - {summary}
- Momentum trading:
    - Investing in stocks that have increased in price the most. 
    - We assess the price changes over the last 12 months, excluding the past month, and select the stock with the highest recent price return over the last year, as the preferred investment.
- Value trading:
    - Investing in stocks that are trading below their true value, i.e. appears undervalued. 
    - A concept called 'Multiples' is used to estimate how valuable a company is.
        - P/E Ratio is a common example of a Multiple.  
    - "You must value the business in order to value the stock." ~ Charlie Munger.

<br/>

#### Possible Future Improvements
- uhh...