
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame


from datetime import datetime
import pandas as pd


def get_crpto_df(from_date,to_date = datetime.now(),crypto_exchange=["BTC/USD", "ETH/USD"]):
    """Gets live Crypto Data

    Keyword arguments:
    :param datetime from_date: initial date
    :param dateime to_date: last date
    :param list tickers -- currency Pairs list to retrieve
    """
    if from_date is None:
        raise AttributeError("from_date is a required field")
    
    client = CryptoHistoricalDataClient()
    request_params = CryptoBarsRequest(
                            symbol_or_symbols=crypto_exchange,
                            timeframe=TimeFrame.Day,
                            start=from_date
                            )
    crypto_df = client.get_crypto_bars(request_params).df

    crypto_dict ={}

    print(crypto_df)

get_crpto_df(datetime(2022, 7, 1))