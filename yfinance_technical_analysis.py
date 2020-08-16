import stonk_functions as sf
from ta import add_all_ta_features
import ta
import pandas as pd

#https://github.com/bukosabino/ta

ticker = 'aapl'

def add_ta_features(ticker):

    try:
        
        # use raw data to do technical analysis, then attach it to processed data
        raw_df = pd.read_csv(sf.get_csv_path('raw', ticker))
        processed_df = pd.read_csv(sf.get_csv_path('processed', ticker))
        
        '''
        # make copy of the processed data
        #feature_df = raw_df.copy()
        
        # create feature columns
        
        feature_df['macd_diff_day'] = ta.trend.macd_diff(raw_df['close'], n_slow=26, n_fast=12, n_sign=9, fillna=False)
        feature_df['macd_diff_week'] = ta.trend.macd_diff(raw_df['close'], n_slow=130, n_fast=60, n_sign=45, fillna=False)
        feature_df['macd_diff_short'] = ta.trend.macd_diff(raw_df['close'], n_slow=18, n_fast=7, n_sign=9, fillna=False)
        feature_df['eligible'] = (feature_df['macd_diff_day'] > 0) & (feature_df['macd_diff_week'] > 0)
        '''
        
        # add all technical analysis features
        feature_df = add_all_ta_features(raw_df
                                       , open="open"
                                       , high="high"
                                       , low="low"
                                       , close="close"
                                       , volume="volume"
                                       )
        
        # drop unnecessary columns
        feature_df = feature_df.drop(['open','high','low','close','adj_close','ticker'], axis=1)
        
        # merge columns to processed data        
        feature_df = processed_df.merge(feature_df, on=['date'])
        
        # write to csv
        feature_df.to_csv(sf.get_csv_path('featured', ticker), index = False)

    except FileNotFoundError:
        print(f'{ticker} no found')
    

    
# execute the function
tickers = sf.get_usable_tickers()
count = 0
for ticker in tickers:
    add_ta_features(ticker)
    count += 1
    print(f'progress {count} / {len(tickers)}')    
    
   
    