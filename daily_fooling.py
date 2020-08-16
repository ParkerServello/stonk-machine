import stonk_functions as sf
import yfinance as yf
import os
import pandas as  pd
import datetime as dt
import ta
from progressbar import ProgressBar

tickers = sf.get_usable_tickers()

start_date = '2020-08-11'
end_date = '2020-08-12'

def get_minutely(ticker):
    
    # write data
    raw_data_path = sf.get_csv_path('raw-minute', ticker)
    new_data = yf.download(ticker, interval = "1m", start = start_date, end = end_date)
    new_data.to_csv(raw_data_path)

# write all the data
for ticker in tickers:
    get_minutely(ticker)
    


# add TA variables
def add_ta_features(ticker):

    raw_data_path = sf.get_csv_path('raw-minute', ticker)
    data = pd.read_csv(raw_data_path)
    
    # macd buy signal
    data['macd_diff'] = ta.trend.macd_diff(data['Close'], n_slow=26, n_fast=12, n_sign=9, fillna=False)
    data['last_macd_diff_1'] = data['macd_diff'].shift(1)
    data['last_macd_diff_2'] = data['macd_diff'].shift(2)
    data['last_macd_diff_3'] = data['macd_diff'].shift(3)
    data['macd_buy'] = [True if (md > md1) & (md <= 0) else False for md, md1, md2, md3 in zip(data['macd_diff'],data['last_macd_diff_1'],data['last_macd_diff_2'],data['last_macd_diff_3'])]
    # (x > y) &
    
    # rsi buy signal
    data['rsi_buy'] = ta.momentum.rsi(data['Close']) <= 30

    # bollinger buy
    data['bolinger_buy'] = data['Close'] <= ta.volatility.bollinger_lband(data['Close'])
    
    # buy signal
    data['buy'] = data['macd_buy'] & data['bolinger_buy'] & data['rsi_buy']
    
    # reduce columns
    data = data[['Datetime', 'buy', 'Close']][data['buy']]
    
    # add ticker
    data['ticker'] = ticker
    
    return(data)
    
all_buys = pd.DataFrame()    
for ticker in tickers:
    all_buys = all_buys.append(add_ta_features(ticker))


    


master_df = pd.DataFrame()
# combine minutely data
pbar = ProgressBar()
for ticker in pbar(tickers):    
    
    # read ticker's feature csv
    feature_path = sf.get_csv_path('featured', ticker)
    feature_df = pd.read_csv(feature_path)                 

    # append ticker data to master
    master_df = master_df.append(feature_df)
    
    


# if bullish    
# buy during day
    
#macd diff positive slope
#rsi below 30
#price below 2std bolinger    
#on bal positive 
