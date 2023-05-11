import os
import sys
import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from utils.MCForecastTools import MCSimulation
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib import interactive
import warnings
warnings.filterwarnings('ignore')



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

    SPDR_sectors = ["XLC", "XLY", "XLP", "XLE", "XLF", "XLV", "XLI", "XLB", "XLRE", "XLK", "XLU","SPY"]
    
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
    
    ticker_dict = {}
    #print(ticker_data["symbol"].unique())
    #create dictionary that contains all tickers and filters out all the columns save for close column
    for ticker in tickers:
        ticker_dict[ticker] = ticker_data[ticker_data["symbol"]==ticker].filter(['close']) #.drop('symbol', axis=1)

    #creates the DataFrame with all elements one next to each other
    ticker_data = pd.concat(ticker_dict.values(),axis=1, keys=tickers)
    
    return ticker_data

def get_stocks_based_on_risk(risk):
    """Gets the list of recommended tickers based on the risk level

    Keyword arguments:
    :param string risk: risk level [high,mid,low]
    """
    # Set the tickers for both the bond and stock portion of the portfolio
    if risk == "high":
        tickers = ["XLK", "XLY", "IWM", "TMF", "TYD"] #50/3 - 40/2 -10/2
        
    elif risk == "mid":
        tickers = ["QQQ", "SPY", "DIA", "TLT", "IEF"]
        
    elif risk == "low":
        tickers = ["SPLV", "NOBL", "VTV", "SHY", "AGG"]

    return tickers

def simulate(ticker_df,risk,simulations_amount,years):
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
            weights=get_weights_based_on_risk("high"),
            num_simulation=simulations_amount,
            num_trading_days=252*years,
        )

    elif risk == "mid":
        MC_simulation = MCSimulation(
            portfolio_data=ticker_df,
            weights=get_weights_based_on_risk("mid"),
            num_simulation=simulations_amount,
            num_trading_days=252*years,
        )

    elif risk == "low":
        MC_simulation = MCSimulation(
            portfolio_data=ticker_df,
            weights=get_weights_based_on_risk("low"),
            num_simulation=simulations_amount,
            num_trading_days=252*years,
        )

    #Initiates cummulative return simulation
    MC_simulation.calc_cumulative_return()

    interactive(False)
    #Plots the simulation results
    fig1, ax1 = plt.subplots()

    MC_simulation.plot_simulation()

    #Plots the result distribution for each iteration.
    MC_simulation.plot_distribution()

    #returns the distribution summary table (statistical results)
    return MC_simulation.summarize_cumulative_return()

def get_weights_based_on_risk(risk):
    if risk=='high':
        return [0.1667, 0.1666, 0.1667, 0.20,0.20, 0.05,0.05]
    elif risk =="mid": 
        return [0.1667, 0.1666, 0.1667, 0.3, 0.20]
    elif risk == "low":
        return [0.20, 0.20, 0.20, 0.20, 0.20]
    
def plot_portfolio_pie(risk,name):
    weights = get_weights_based_on_risk(risk)
    stocks = get_stocks_based_on_risk(risk)

    if risk == "high":
        stocks + ['BTC/USD'] + ['ETH/USD']
    
    fig1, ax1 = plt.subplots()
    ax1.pie(weights , labels=stocks, autopct='%1.1f%%',shadow=True, startangle=90) #,title=f"{name}'s {risk} Risk Portofolio"
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.show()