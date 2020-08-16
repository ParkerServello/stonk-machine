import stonk_functions as sf
import yfinance as yf
import pandas as  pd
import datetime as dt

tickers = sf.get_usable_tickers()

tickers = [tickers]

start_date = '2020-08-11'
end_date = '2020-08-12'

new_data = yf.download(ticker, interval = "1m", group_by = 'ticker', start = start_date, end = end_date)
