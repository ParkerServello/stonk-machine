import datetime as dt
from selenium import webdriver
import ta
import pandas as pd
import pandas_market_calendars as mcal

# don't give warnings on indexing
pd.options.mode.chained_assignment = None

# get today
today = str(dt.datetime.date(dt.datetime.now()))

def get_stonk_project_path():
    
    # repository path
    return r'C:\Users\VanillaBean\Documents\PyProjects\stonk-machine'
      
def get_tickers():
    
    # specify that we don't want to open a window
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    
    # launch the driver
    driver = webdriver.Firefox(options=options)

    # go to the website we're scraping
    url = 'https://www.slickcharts.com/sp500'
    driver.get(url)
    
    # get the page html
    html = driver.page_source
    
    # parse html to get tickers
    tickers = html.split('<td><a href="/symbol/')[1:-2]
    
    # trim html code off of the tickers
    spy_list = []
    for ticker in tickers:        
        ticker = ticker.split('">')[0]
        ticker = ''.join(char for char in ticker if char.isalnum())
        spy_list.append(ticker)
        
    # remove duplicates and make lowercase        
    tickers = list(set(spy_list))    
    tickers = [ticker.lower() for ticker in tickers]

    driver.close()
    
    return(tickers)

def get_csv_path(path, ticker=''):
    
    '''
    :path: string - ['raw', 'featured']
    :ticker: string
    '''

    # get the argument's directory
    if path == 'raw':
        path = 'raw_data'    
    elif path == 'featured':
        path =  'featured_data'        
    elif path == 'master':
        path = 'master_data'
    else:
        print("paths: 'raw', 'featured', 'master'")   
    
    # attach stonk project directory
    prefix = get_stonk_project_path() + '\\'
    path = prefix + path + ticker + '.csv'
    
    return path

def add_ta_features(df):
    
    # macd buy signal
    df['macd_diff'] = ta.trend.macd_diff(df['Close'], n_slow=26, n_fast=12, n_sign=9, fillna=False)
    df['macd_diff_lag_1'] = df['macd_diff'].shift(1)
    df['macd_diff_lag_2'] = df['macd_diff'].shift(2)
    df['macd_buy'] = [True if (md > md1) else False for md, md1, md2 in zip(df['macd_diff'],df['macd_diff_lag_1'],df['macd_diff_lag_2'])]

    # rsi buy signal
    df['rsi_indicator'] = ta.momentum.rsi(df['Close']) <= 30
    df['rsi_indicator_lag_1'] = df['rsi_indicator'].shift(1)
    #df['rsi_indicator_lag_2'] = df['rsi_indicator'].shift(2)
    df['rsi_buy'] = [True if any([a,b]) else False for a,b in zip(df['rsi_indicator'],df['rsi_indicator_lag_1'])]
    
    # bollinger buy
    df['bolinger_indicator'] = df['Close'] <= ta.volatility.bollinger_lband(df['Close'], ndev = 3)
    df['bolinger_indicator_lag_1'] = df['bolinger_indicator'].shift(1)
    #df['bolinger_indicator_lag_2'] = df['bolinger_indicator'].shift(2)
    #df['bolinger_indicator_lag_3'] = df['bolinger_indicator'].shift(3)
    #df['bolinger_indicator_lag_4'] = df['bolinger_indicator'].shift(4)
    df['bolinger_buy'] = [True if any([a,b]) else False for a,b in zip(df['bolinger_indicator'],df['bolinger_indicator_lag_1'])]

    
    
    # buy signal
    df['buy'] = df['macd_buy'] & df['bolinger_buy'] & df['rsi_buy']
        
    return(df)
        

def create_day_start_df(date, minutes):
    
    # get data path
    data_prefix = get_stonk_project_path() + '\\data\\raw_data_'
    
    # get previous trading day
    nyse = mcal.get_calendar('NYSE')
    dates = [date.strftime('%Y-%m-%d') for date in nyse.schedule(start_date='2020-08-01', end_date='2020-08-27').index]
    previous_date = dates[dates.index(date)-1]
    
    output_df = pd.DataFrame()
    for minute in range(390-minutes,390):
        
        # append a minute of data to the output
        minute_df = pd.read_parquet(data_prefix + previous_date + '\\Minute=' + str(minute))
        output_df = output_df.append(minute_df)
        
    # append the first minute of today
    minute_df = pd.read_parquet(data_prefix + date + '\\Minute=0')    
    output_df = output_df.append(minute_df)
    
    return(output_df)    
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    