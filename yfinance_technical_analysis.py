import stonk_functions as sf
from ta import add_all_ta_features
import pandas as pd

# use raw data to do technical analysis, then attach it to processed data
raw_df       = pd.read_csv(sf.get_csv_path('raw','msft'))
processed_df = pd.read_csv(sf.get_csv_path('processed','msft'))

# create feature columns
feature_df = add_all_ta_features(raw_df
                               , open="open"
                               , high="high"
                               , low="low"
                               , close="close"
                               , volume="volume"
                               )

# drop original high/low/close columns
feature_df = feature_df.drop(['high', 'low', 'open', 'close', 'volume', 'adj_close'], axis=1)


# merge with processed and write
processed_df = processed_df.merge(feature_df, on = ['date', 'ticker'])
processed_df.to_csv(sf.get_csv_path('processed','msft'), index = False)
