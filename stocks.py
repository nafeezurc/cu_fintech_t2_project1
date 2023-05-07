import os
import sys
import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from MCForecastTools import MCSimulation
import yfinance as yf
from datetime import datetime, timedelta


def get_stocks_df(risk="high",
                  start_date=pd.Timestamp("2018-01-01", tz="America/New_York").isoformat(),
                  end_date=(pd.Timestamp.today(tz="America/New_York")-pd.Timedelta(days=1)).isoformat()):
    """Gets a set of ticker data from an specific date

    Keyword arguments:
    :param string risk: risk level [high,mid,low]
    :param datetime start_date: initial date
    :param dateime end_date: last date
    """

    # Load the environment variables from the .env file
    #by calling the load_dotenv function
    load_dotenv('api.env')
    
    # Set the variables for the Alpaca API and secret keys
    alpaca_api_key = os.getenv("ALPACA_API_KEY")
    alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

    print(pd.Timestamp(datetime.now()-timedelta(days=1)))

    # Create the Alpaca tradeapi.REST object
    api = tradeapi.REST(
        alpaca_api_key,
        alpaca_secret_key,
        api_version = "v2"
    )

    SPDR_sectors = ["XLC", "XLY", "XLP", "XLE", "XLF", "XLV", "XLI", "XLB", "XLRE", "XLK", "XLU"]
    
    tickers = get_stocks_based_on_risk(risk)

    # Set timeframe to 1Day
    timeframe = "1Day"

    # Use the Alpaca get_bars function to get current closing prices the portfolio
    # Be sure to set the `df` property after the function to format the response object as a DataFrame
    ticker_data = api.get_bars(
        tickers,
        timeframe,
        start=start_date,
        end=end_date
    ).df
    print(ticker_data)
    ticker_dict = {}

    for ticker in SPDR_sectors:
        ticker_dict[ticker] = ticker_data[ticker_data["symbol"]==ticker].drop('symbol', axis=1)

    ticker_data = pd.concat(ticker_dict.values(),axis=1, keys=SPDR_sectors)

    return ticker_data


def get_stocks_column_value(ticker_df,column):
    """Selects an specific column from a multi ticker DataFrame

    Keyword arguments:
    :param DataFrame ticker_df: Contains a ticker DataFrame with multiple tickers
    :param string risk: risk level [high,mid,low]
    """
    dict_close = {}

    for ticker in ticker_df:
        dict_close[ticker]=ticker_df[ticker].filter([column])

    return pd.concat(dict_close.values(),axis=1,keys=dict_close.keys())



def get_stocks_based_on_risk(risk):
    """Gets the list of recommended tickers based on the risk level

    Keyword arguments:
    :param string risk: risk level [high,mid,low]
    """
    # Set the tickers for both the bond and stock portion of the portfolio
    if risk == "high":
        tickers = ["XLK", "XLY", "IWM", "TMF", "TYD"]
        
    elif risk == "mid":
        tickers = ["QQQ", "SPY", "DIA", "TLT", "IEF"]
        
    elif risk == "low":
        tickers = ["SPLV", "NOBL", "VTV", "SHY", "AGG"]

    return tickers

def simulate(ticker_df,risk,years):
    """Gets a list of tickers from an specific date

    Keyword arguments:
    :param DataFrame ticker_df: Contains a ticker DataFrame with multiple tickers
    :param string risk: risk level [high,mid,low]
    :param numeric years: investment timeline
    """
    # Create simulation object for each risk level
    if risk == "high":
        MC_simulation = MCSimulation(
            portfolio_data=ticker_df,
            weights=[0.15, 0.15, 0.15, 0.15,0.20, 0.20],
            num_simulation=500,
            num_trading_days=252*years,
        )

    if risk == "mid":
        MC_simulation = MCSimulation(
            portfolio_data=ticker_df,
            weights=[0.15, 0.15, 0.15, 0.15, 0.20, 0.20],
            num_simulation=500,
            num_trading_days=252*years,
        )

    if risk == "low":
        MC_simulation = MCSimulation(
            portfolio_data=ticker_df,
            weights=[0.20, 0.20, 0.20, 0.20, 0.20],
            num_simulation=500,
            num_trading_days=252*years,
        )

    #Initiates cummulative return simulation
    MC_simulation.calc_cumulative_return()

    #Plots the simulation results
    MC_simulation.plot_simulation()

    #Plots the result distribution for each iteration.
    MC_simulation.plot_distribution()

    #returns the distribution summary table (statistical results)
    return MC_simulation.summarize_cumulative_return()