import yfinance as yf
import datetime as dt
from retrying import retry
import os
from selenium import webdriver

today = str(dt.datetime.date(dt.datetime.now()))

def get_stonk_project_path():
    
    # repository path
    return r'C:\repos\stonk-machine\'

def format_column_names(df):
    
    # lowercase and replace spaces with underscores
    rename_dict = {}
    for col in list(df.columns):
        new_col = col.lower().replace(' ', '_')
        rename_dict[col] = rename_dict.setdefault(col, new_col)
    return df.rename(columns = rename_dict)
      
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

def get_usable_tickers():
    
    # get the list of csv we have
    raw_data_path = get_stonk_project_path() + '\\raw-data'
    ticker_csv_list = [ticker.replace('.csv', '') for ticker in os.listdir(raw_data_path)]
    
    # if we have a csv for the ticker keep it
    return [ticker for ticker in get_tickers() if ticker in ticker_csv_list]  

    

def get_csv_path(path, ticker = ''):
    
    '''
    :path: string - ['raw', 'processed', 'input', 'featured', 'master']
    :ticker: string
    '''
    
    # certain paths require a ticker
    if path in ['raw', 'processed', 'featured', 'raw-minute'] and ticker == '':
        print('Path requires a ticker')
        return
    
    # get the argument's directory
    if path == 'raw-minute':
        path = '\\raw-minute\\'
    elif path == 'raw':
        path = '\\raw-data\\'
    elif path == 'processed':
        path =  '\\processed-data\\'
    elif path == 'featured':
        path =  '\\featured-data\\'        
    elif path == 'input':
        path = '\\model-input\\input_' + today
    elif path == 'master':
        path = '\\master'
    else:
        print("paths: 'raw', 'processed', 'input', 'featured', 'master'")   
    
    # attach stonk project directory
    prefix = get_stonk_project_path()
    path = prefix + path + ticker + '.csv'
    
    return path
    

def retry_on_indexerror(exc):
    return isinstance(exc, IndexError)

@retry(retry_on_exception=retry_on_indexerror)
def get_today_open(ticker):

    today_data = yf.download(
                tickers = ticker,
                period = "1d",
                interval = "1m",
                group_by = 'ticker',
                )
    
    return today_data[today_data.index == today_data.index.min()]['Open'][0]