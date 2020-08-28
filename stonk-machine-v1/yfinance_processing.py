import pandas as pd
import stonk_functions as  sf

#ticker = 'msft'

def process_data(ticker):
    # prefixes for raw/processed
    read_path = sf.get_csv_path('raw', ticker)
    write_path = sf.get_csv_path('processed', ticker)
    
    # read/format data
    raw_data = pd.read_csv(read_path)

    # make a copy of the raw_data
    processed_data = raw_data.copy()
    
    # create next_open column
    processed_data['next_open'] = processed_data['open'].shift(-1)
    
    # put today's open on last row
    today_open = sf.get_today_open(ticker)
    processed_data.iloc[-1, processed_data.columns.get_loc('next_open')] = today_open
    
    # standardize volume
    processed_data['standard_volume'] = (processed_data['volume'] - processed_data['volume'].mean()) \
                                          / processed_data['volume'].std()
                                  
    # convert relevant columns to percent difference from open
    for col in ['high', 'low', 'close', 'next_open']:
        processed_data[col] = (processed_data[col] / processed_data['open'] - 1) * 100

    # create target open to open
    processed_data['next_oto'] = processed_data['next_open'].shift(-1)
    
    # drop unnecessary few columns
    processed_data = processed_data.drop(['adj_close', 'volume', 'next_open'], axis = 1) 

    # write data to csv
    processed_data.to_csv(write_path, index=False)  
    
# process data
for ticker in sf.get_usable_tickers():
    process_data(ticker)


