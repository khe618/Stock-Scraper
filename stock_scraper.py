import requests
import pandas as pd
import time
import sys
from datetime import datetime

API_KEY = "EUYE90FIE1U4Q0UD"
valid_intervals = ["1", "5", "15", "30", "60"]

with open('stock_symbols.txt') as f:
    stock_symbols = f.read()
stock_symbols = stock_symbols.split("\n")
stock_symbols = [symbol for symbol in stock_symbols if len(symbol) > 0]

def get_historical_data(symbol):
    """
    Scrapes the Alpha Vantage API for historical data

    Args:
        symbol (str): The stock symbol to query for
    """
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="
    url += symbol
    url += "&outputsize=full&apikey=" + API_KEY
    data = requests.get(url)
    json_data = data.json()
    time_series_data = json_data['Time Series (Daily)']
    time_series_df = pd.DataFrame.from_dict(time_series_data, orient = "index")
    return time_series_df
    
def get_intraday_stock_data(symbol, time_interval, df):
    """
    Scrapes the Alpha Vantage API for real time stock data

    Args:
        symbol (str): The stock symbol to query for
        time_interval (str): The time interval between data points. Accepted
        values are '1min', '5min', '15min', '30min' and '60min'
        df (pandas.core.frame.DataFrame): Pandas dataframe to write to

    Returns:
        df (pandas.core.frame.DataFrame): Updated dataframe
    """
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="
    url += symbol
    url += "&interval=" + time_interval
    url += "&apikey=" + API_KEY
    data = requests.get(url)
    json_data = data.json()
    time_series_key = "Time Series (" + time_interval + ")"
    time_series_data = json_data[time_series_key]
    time_series_df = pd.DataFrame.from_dict(time_series_data, orient = "index")
    #if empty dataframe, return all the data
    if df.shape[0] == 0:
        return time_series_df
    #iterate through the data frame to find the first new data point
    new_data_index = False
    last_row_index = df.tail(1).index
    for index, row in time_series_df.iterrows():
        if (index > last_row_index)[0]:
            new_data_index = index
            break
    else:
        return df
    new_data_df = time_series_df[new_data_index:]
    new_data_df = df.append(new_data_df)
    return new_data_df

def get_company_info(symbol):
    """
    Scrapes the IEX API for company info

    Args:
        symbol (str): The stock symbol to query for

    Returns:
        df (pandas.core.frame.DataFrame): Dataframe containing the company info
    """
    url = "https://api.iextrading.com/1.0/stock/"
    url += symbol
    url += "/stats"
    data = requests.get(url)
    json_data = data.json()
    company_info_df = pd.DataFrame(json_data, index = [0])
    return company_info_df

if __name__ == '__main__':
    if len(sys.argv) == 1 or "-h" in sys.argv:
        print('''
        Stock data scraper

        Either fetches historical daily data for the past 20 years,
        or automatically fetches intraday data at specified time intervals

        One required argument: the number of minutes between updates (1, 5,
        15, 30, 60) OR "historical" to get historical data
        ''')
        sys.exit()
    parameter = sys.argv[-1]
    if parameter == "historical":
        for symbol in stock_symbols:
            print("Downloading historical data for " + symbol)
            file_path = symbol + "_historical_stock_data.csv"
            df = get_historical_data(symbol)
            df.to_csv(file_path)
            #sleep to avoid exceeding API call limit
            time.sleep(15)
    elif parameter == "info":
        if len(stock_symbols) > 0:
            file_path = "company_info.csv"
            df = get_company_info(stock_symbols[0])
            for i in range(1, len(stock_symbols)):
                company_info = get_company_info(stock_symbols[i])
                df = df.append(company_info, sort=False)
            df.to_csv(file_path, index = False)
            print("Successfully downloaded company info")
    elif parameter in valid_intervals:
        interval = parameter + "min"
        seconds = int(parameter) * 60
        while(True):
            print(datetime.now())
            for symbol in stock_symbols:
                file_path = symbol + "_intraday(" + interval + ")_stock_data.csv"
                #initialize dataframe
                df = pd.DataFrame(columns=["1. open", "2. high", "3. low", "4. close", "5. volume"])
                #use this to load csv file
                #df = pd.read_csv(file_path, index_col = 0)
                df = get_intraday_stock_data(symbol, interval, df)
                df.to_csv(file_path)
                #sleep to avoid exceeding API call limit
                time.sleep(15)
            time.sleep(seconds)    
        
