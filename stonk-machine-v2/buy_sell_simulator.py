import stonk_functions_v2 as sf
import pandas as  pd
import datetime as dt
import pandas_market_calendars as mcal

data_prefix = f'C:\\repos\\stonk-machine\\data\\'



# build date lists using only trading days
#date_df = pd.DataFrame()
#date_df['date'] = nyse.schedule(start_date='2020-08-13', end_date='2020-08-17').index
#date_df['next_date'] = date_df['date'] + dt.timedelta(1)
dates = mcal.get_calendar('NYSE').schedule(start_date='2020-08-13', end_date='2020-08-17').index

date = dates[1]

# set intitial variables
state = 'buy'
data_dict = {}
buy_minutes = pd.DataFrame()

for date in date_df['date']:
    
    date = date.strftime('%Y-%m-%d')
    
    # get the previous days last few minutes
    minutes_df = sf.create_day_start_df(date, minutes=30)
    
    # get list of tickers
    tickers = set(minutes_df['Ticker'])
    
    # store ticker dataframes
    for ticker in tickers:
        data_dict[ticker] = minutes_df[minutes_df['Ticker'] == ticker]
    
    minute = 0
        
    while state == 'sell':
        
        
    
    while state == 'buy':
    
        for ticker in tickers:
            
            # compue TA features
            current_data = sf.add_ta_features(data_dict[ticker])            
            
            # check for buy indicator
            if current_data['buy'][-1] == True:
                
                # store row
                buy_minutes = buy_minutes.append(data_dict[ticker].tail(1))

                # switch to sell mode
                state = 'sell'
                
            # if we didn't buy, add a minute and recompute TA features
            else:
                
                
                    
                    
                

today_df = pd.DataFrame()

# keep the current min date and stop if there's no buy signal before it
# add TA variables to each date csv
cnt = 0
for date in date_df['date']:
    
    # read raw data
    date = date.strftime('%Y-%m-%d')
    raw_df = pd.read_parquet(data_prefix + f'raw_data_{date}')
    
    ta_df = pd.DataFrame()
    for ticker in tickers:
        
        # take ticker master_raw_df
        ticker_df = raw_df[raw_df['ticker'] == ticker].reset_index(drop=True)
                        
        # calculate TA variables
        ticker_df = sf.add_ta_features(ticker_df)
        
        # append to master_df
        ta_df = ta_df.append(ticker_df)
        
        # progress
        cnt += 1
        print(f"{cnt} / {len(tickers) * len(date_df['date'])}")
        
    # write to csv   
    ta_df.to_parquet(data_prefix + f'ta_data_{date}', index=False)
    
    
buy_df = pd.DataFrame()
for date in date_df['date']:
    
    # turn date to string
    date = date.strftime('%Y-%m-%d')
    
    # read data
    ta_df = pd.read_parquet(data_prefix + f'ta_data_{date}')
        
    # get first buy time and add it to the buy log
    buy_row = ta_df[ta_df['buy'] == True].sort_values('Datetime').reset_index(drop=True).iloc[0]    
    buy_df = buy_df.append(buy_row)



























