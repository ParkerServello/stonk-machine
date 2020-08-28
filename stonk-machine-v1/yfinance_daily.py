import yfinance as yf
import os
import pandas as  pd
import datetime as dt
import stonk_functions as sf

def update_raw_data(ticker):
    
    try:
            
        # create csv path for ticker
        raw_data_path = sf.get_csv_path('raw', ticker)
        
        # check if we have data for the ticker
        initializing = not os.path.isfile(raw_data_path)
        
        # if this is the first time handling this ticker, we'll bring in data starting from 2015
        if initializing:
            start_date = '2015-01-01'
            data = pd.DataFrame()
        # if this isn't the first run, look at the last time we saw it then bring in data starting after that
        else:
            # read the data and find last time it was updated
            data = pd.read_csv(raw_data_path)
            last_seen = data['date'].max()
        
            # use the day after last_seen to start
            start_date = dt.datetime.strptime(last_seen, '%Y-%m-%d') + dt.timedelta(days=1)
            start_date = dt.datetime.strftime(start_date, '%Y-%m-%d')
            
        # use today as end_date
        end_date =  str(dt.datetime.date(dt.datetime.now() + dt.timedelta(1)))
        
        # download data
        new_data = yf.download(ticker, start = start_date, end = end_date)
        
        # turn date into column
        new_data = new_data.reset_index()
        
        # lowercase columns names and replace space with underscore
        new_data = sf.format_column_names(new_data)
    
        # remove duplicates, yahotodayo returns an extra row for yesterday if ran before market  
        new_data = new_data.loc[~new_data['date'].duplicated(keep='first')]
        
        # format date column
        new_data['date'] = new_data['date'].apply(lambda date: dt.datetime.strftime(date, '%Y-%m-%d'))
            
        # add ticker column
        new_data['ticker'] = ticker
        
        # save data
        if initializing:
            # if we're missing major data (less than 30 days), don't write 
            if new_data.size > 30:
                new_data.to_csv(raw_data_path, index = False)
        else:
            # append data and remove duplicates, then overwrite
            new_data = data.append(new_data)
            new_data = new_data.sort_values('volume').groupby(['date']).first().reset_index()
            new_data.to_csv(raw_data_path, index = False)
            
    except (IndexError, TypeError):
        print(f'{ticker} has no data')
        
# update all ticker data
for ticker in sf.get_tickers():
    update_raw_data(ticker)
    
    