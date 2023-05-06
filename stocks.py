import os
import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from MCForecastTools import MCSimulation
import yfinance as yf
from datetime import datetime, timedelta

# Load the environment variables from the .env file
#by calling the load_dotenv function
load_dotenv('api.env')

api = None
ticker_data = None

def get_stocks_df(risk="high",start_date=pd.Timestamp("2018-01-01", tz="America/New_York").isoformat(),end_date=datetime.now()-timedelta(days=1)):
    # Set the variables for the Alpaca API and secret keys
    alpaca_api_key = os.getenv("ALPACA_API_KEY")
    alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

    # Create the Alpaca tradeapi.REST object
    api = api or tradeapi.REST(
        alpaca_api_key,
        alpaca_secret_key,
        api_version = "v2"
    )

    SPDR_sectors = ["XLC", "XLY", "XLP", "XLE", "XLF", "XLV", "XLI", "XLB", "XLRE", "XLK", "XLU"]

    # Use the Alpaca get_bars function to get current closing prices the portfolio
    # Be sure to set the `df` property after the function to format the response object as a DataFrame
    
    tickers = get_stocks_based_on_risk(risk)

    # Set timeframe to 1Day
    timeframe = "1Day"

    # Format current date as ISO format
    # Set both the start and end date at the date of your prior weekday 
    # This will give you the closing price of the previous trading day
    # Alternatively you can use a start and end date of 2020-08-07
    #start_date = pd.Timestamp("2018-01-01", tz="America/New_York").isoformat()
    #end_date = pd.Timestamp("2023-05-04", tz="America/New_York").isoformat()
    
    ticker_data = ticker_data or api.get_bars(
        tickers,
        timeframe,
        start=start_date,
        end=end_date
    ).df

    ticker_dict = {}

    for ticker in SPDR_sectors:
        ticker_dict[ticker] = ticker_data[ticker_data[ticker]==ticker].drop('symbol', axis=1)

    ticker_data = pd.concat(ticker_dict.values(),axis=1, keys=SPDR_sectors)

    return ticker_data


def get_stocks_column_value(ticker_dict,column):
    dict_close = {}

    for ticker in ticker_dict:
        dict_close[ticker]=ticker_dict[ticker].filter([column])

    return pd.concat(dict_close.values(),axis=1,keys=dict_close.keys())



def get_stocks_based_on_risk(risk):
    # Set the tickers for both the bond and stock portion of the portfolio
    if risk == "high":
        tickers = ["XLK", "XLY", "IWM", "TMF", "TYD"]
        
    elif risk == "mid":
        tickers = ["QQQ", "SPY", "DIA", "TLT", "IEF"]
        
    elif risk == "low":
        tickers = ["SPLV", "NOBL", "VTV", "SHY", "AGG"]

    return tickers


    