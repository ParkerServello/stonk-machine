import yfinance as yf
import os
import pandas as  pd
import datetime as dt
import stonk_functions as sf


# create csv path for ticker
raw_data_path = sf.get_csv_path('raw', ticker)

start_date, end_date = '2020-08-01', '2020-08-31'


# get available tickers
tickers = sf.get_tickers()

tickers = tickers[:10]

# download data from yahoo finance
new_data = yf.download(tickers, start = start_date, end = end_date)
