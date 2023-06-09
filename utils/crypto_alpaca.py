
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame


from datetime import datetime,timedelta
import pandas as pd


def get_crypto_df(from_date=datetime(2018,1,1),
                  to_date=datetime.now()-timedelta(days=1),
                  crypto_exchange=["BTC/USD", "ETH/USD"]):
    """Gets live Crypto Data

    Keyword arguments:
    :param datetime from_date: initial date
    :param dateime to_date: last date
    :param list crypto_exchange -- currency Pairs list to retrieve
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
    crypto_df=crypto_df.reset_index().set_index('timestamp')

    crypto_dict = {}

    for crypto in crypto_exchange:
        crypto_dict[crypto] = crypto_df[crypto_df["symbol"]==crypto].filter(['close'])#.drop('symbol',axis=1)

    final_df = pd.concat(crypto_dict.values(),axis=1,keys=crypto_exchange)

    return final_df