
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame


from datetime import datetime

client = CryptoHistoricalDataClient()
request_params = CryptoBarsRequest(
                        symbol_or_symbols=["BTC/USD", "ETH/USD"],
                        timeframe=TimeFrame.Day,
                        start=datetime(2018, 1, 1)
                        )
bars = client.get_crypto_bars(request_params)


print(bars)