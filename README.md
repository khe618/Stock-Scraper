"# Stock-Scraper" 

This scraper can be used in command line to download stock prices in real-time, as well as historical data, and can also retrieve company information such as P/E ratio, EBITDA, etc.

To use, enter <code>python stock_scraper.py historical</code> to download historical stock data,
<code>python stock_scraper.py info</code> to download company info,
<code>python stock_scraper.py TIME_INTERVAL</code> where TIME_INTERVAL = {1, 15, 30, 60} to download stock data in real-time. TIME_INTERVAL represents the number of minutes between updates.

The stock data is obtained from the Alpha Venture API, whereas the company info is obtained from the IEX API. To set which companies you want to query for, edit the list of stock symbols in stock_symbols.txt. For whichever option you select, the data is written to a CSV file located in the same directory as stock_scraper.py
