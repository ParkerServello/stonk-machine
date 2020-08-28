import stonk_functions_v2 as sf
import pandas as  pd
import pandas_market_calendars as mcal
import sys

data_prefix = f'C:\\Users\\VanillaBean\\Documents\\PyProjects\\stonk-machine\\data\\raw_data_'



# build date lists using only trading days and convert to strings
dates = mcal.get_calendar('NYSE').schedule(start_date='2020-08-01', end_date='2020-08-25').index
dates = [date.strftime('%Y-%m-%d') for date in dates]

# set intitial variables
state = 'buy'
data_dict = {}
buy_minutes = pd.DataFrame()
sell_prices = []

for date in dates:
    
    # reset the minute counter
    minute = 1
    
    # get the number of minutes for that day, some days the market closes early
    
    # get the previous day's last few minutes
    minutes_df = sf.create_day_start_df(date, minutes=30)
    
    # get list of tickers
    tickers = set(minutes_df['Ticker'])
    
    # store ticker dataframes in a dictionary {ticker:df}
    for ticker in tickers:
        data_dict[ticker] = minutes_df[minutes_df['Ticker'] == ticker]
        
    while state == 'sell':
        
        # sell at the beginning of the day for testing, we'll play with conditions
        
        # get the ticker to buy
        ticker = list(buy_minutes['Ticker'])[-1]
        
        # store the sell data
        sell_prices.append(list(data_dict[ticker]['Close'])[-1])
                
        # switch states
        state = 'buy'
    
    while state == 'buy':
        
        # don't buy the last day
        if date == dates[-1]:
            break
        
        # read the next minute's worth of data so we can append it to each ticker
        minute_df = pd.read_parquet(data_prefix + date + f'\\Minute={minute}')  
        minute += 1
        
        # progress print
        sys.stdout.write(f"\r{date} {minute}")
        sys.stdout.flush()
        
        for ticker in tickers:
            
            # compute TA features
            current_data = sf.add_ta_features(data_dict[ticker])            
            
            # check for buy indicator
            if list(current_data['buy'])[-1] == True:
                
                # store row
                buy_minutes = buy_minutes.append(data_dict[ticker].tail(1), sort=False)

                # switch to sell mode
                state = 'sell'
                
                # stop searching for a buy
                break
                
            # if we didn't buy, add a minute of data
            else:
                data_dict[ticker] = data_dict[ticker].append(minute_df[minute_df['Ticker'] == ticker], sort=False)
                     
    #                
    print()
        

# calculate tendies                
buy_minutes['Change'] = sell_prices / buy_minutes['Close']
                   
# performance
buy_minutes['Change'].product()
           




# might want to partition by ticker so we don't have to read in all tickers for


        












