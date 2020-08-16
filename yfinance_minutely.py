import stonk_functions as sf
import yfinance as yf
import pandas as  pd
import datetime as dt
import os
import numpy as np

# go to where the gecko driver is
os.chdir(sf.get_stonk_project_path())

# get tickers
tickers = sf.get_tickers()

# for testing
tickers = tickers[:10]

# start end dates
start_date = '2020-08-11'
end_date = '2020-08-12'

# write path
master_raw_path = sf.get_csv_path('master')

# check to see if master exists
initial_run = not os.path.exists(master_raw_path)  

# get data starting...
if initial_run:
    
    # initialize master_raw
    master_raw_df = pd.DataFrame()
    
    # get all the data
    new_wide_df = yf.download(tickers, interval = "1m", group_by = 'ticker', start = '2020-08-11', end='2020-08-12')

else:    
    # read the current master
    master_raw_df = pd.read_csv(master_raw_path)
    
    # get the last minute of data that we currently have
    start_time = master_raw_df['datetime'].max()
    
    # convert to from datetime64[ns, America/New_York] to datetime 
    start_time = dt.datetime.utcfromtimestamp((np.datetime64(start_time) - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's'))

    # ping yahoo for data
    new_wide_df = yf.download(tickers, interval = "1m", group_by = 'ticker', start=start_time)


# narrow the data
new_narrow_df = pd.DataFrame()
for ticker in tickers:
    ticker_df = new_wide_df.pop(ticker.upper())
    ticker_df.insert(0, 'ticker', ticker)
    new_narrow_df = new_narrow_df.append(ticker_df)

# add datetime as a column
new_narrow_df = new_narrow_df.reset_index().rename({'Datetime':'datetime'}, axis=1) 

# change to datetime
new_narrow_df['datetime'] = pd.Series(new_narrow_df['datetime'].astype(str).map(lambda t: t[:19])).astype(str)

# append to master
master_raw_df = master_raw_df.append(new_narrow_df)

# put ticker rows together
master_raw_df = master_raw_df.sort_values(['ticker', 'datetime'], ascending=False)
    
# write the data
master_raw_df.to_csv(master_raw_path, index=False)
