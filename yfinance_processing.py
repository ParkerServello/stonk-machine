import pandas as pd
import stonk_functions as  sf

def process_data(ticker):
    # prefixes for raw/processed
    read_path = sf.get_csv_path('raw', ticker)
    write_path = sf.get_csv_path('processed', ticker)
    
    # read/format data
    data = pd.read_csv(read_path)

    # create next_open column
    data['next_open'] = data['open'].shift(-1)
    
    # put today's open on last row
    today_open = sf.get_today_open(ticker)
    data.iloc[-1, data.columns.get_loc('next_open')] = today_open
    
    # standardize volume
    data['standard_volume'] = (data['volume'] - data['volume'].mean()) \
                                  / data['volume'].std()
    
    # convert relevant columns to percent difference from open
    for col in ['high', 'low', 'close', 'next_open']:
        data[col] = (data[col] / data['open'] - 1) * 100
    
    # drop unnecessary few columns
    data = data.drop(['open', 'adj_close', 'volume'], axis = 1) 
    
    # create target open to open then buy, if oto gain is greater than 2% we'll buy
    data['oto'] = data['next_open'].shift(-1)

    # write data to csv
    data.to_csv(write_path, index=False)
    
# process data
for ticker in sf.get_tickers():
    process_data(ticker)

