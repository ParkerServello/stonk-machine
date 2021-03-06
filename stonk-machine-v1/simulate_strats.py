import ta
import stonk_functions_v2 as sf
import yfinance as yf
import os
import pandas as  pd
import datetime as dt
import pandas_market_calendars as mcal

data_prefix = f'C:\\repos\\stonk-machine\\data\\'

# get yahoo finance download arguments: ticker list, end date, start date
tickers = sf.get_tickers()

# build date lists using only trading days
nyse = mcal.get_calendar('NYSE')
date_df = pd.DataFrame()
date_df['date'] = nyse.schedule(start_date='2020-08-13', end_date='2020-08-17').index
date_df['next_date'] = date_df['date'] + dt.timedelta(1)

# get the raw data then write it out so we don't have to ping yahoo finance every the time
for date, next_date in zip(date_df['date'], date_df['next_date']):

    # get the data then write it out so we don't have to ping yahoo finance every the time
    raw_df = yf.download(tickers, interval="1m", group_by='ticker', start=date, end=next_date)
    
    master_raw_df = pd.DataFrame()
    for ticker in tickers:
        
        # take ticker from raw_df and give it a ticker column and
        ticker_df = raw_df.pop(ticker.upper())
        ticker_df.insert(0, 'ticker', ticker)
        
        # give it a datetime column and convert it to string
        ticker_df = ticker_df.reset_index()
        ticker_df['Datetime'] = pd.Series(ticker_df['Datetime'].astype(str).map(lambda t: t[:19])).astype(str)
        
        # fill na
        ticker_df = ticker_df.ffill()
        
        # append to master_df
        master_raw_df = master_raw_df.append(ticker_df)
    
    # turn date to string and write csv
    date = date.strftime('%Y-%m-%d')
    master_raw_df.to_csv(data_prefix + f'raw_data_{date}.csv', index=False)


# keep the current min date and stop if there's no buy signal before it
# add TA variables to each date csv
for date in date_df['date']:
    
    # read raw data
    date = date.strftime('%Y-%m-%d')
    raw_df = pd.read_csv(data_prefix + f'raw_data_{date}.csv')
    
    ta_df = pd.DataFrame()
    for ticker in tickers:
        
        # take ticker master_raw_df
        ticker_df = raw_df[raw_df['ticker'] == ticker].reset_index(drop=True)
                        
        # calculate TA variables
        ticker_df = sf.add_ta_features(ticker_df)
        
        # append to master_df
        ta_df = ta_df.append(ticker_df)
    
    # write to csv   
    ta_df.to_csv(data_prefix + f'ta_data_{date}.csv', index=False)


buy_df = pd.DataFrame()
for date in date_df['date']:
    
    # turn date to string
    date = date.strftime('%Y-%m-%d')
    
    # read data
    ta_df = pd.read_csv(data_prefix + f'ta_data_{date}.csv')
        
    # get first buy time and add it to the buy log
    buy_row = ta_df[ta_df['buy'] == True].sort_values('Datetime').reset_index(drop=True).iloc[0]    
    buy_df = buy_df.append(buy_row)



























