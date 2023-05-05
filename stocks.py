import pandas as pd
import numpy as np
from pathlib import Path
import yfinance as yf

tqqq = yf.Ticker("TQQQ")
tqqq_hist = tqqq.history()
tqqq_closing = pd.DataFrame(tqqq_hist["Close"])


