import stonk_functions as sf
import pandas as pd
from progressbar import ProgressBar


# get tickers and initialize master
tickers = sf.get_usable_tickers()
master_df = pd.DataFrame()

pbar = ProgressBar()
for ticker in pbar(tickers):    
    
    # read ticker's feature csv
    feature_path = sf.get_csv_path('featured', ticker)
    feature_df = pd.read_csv(feature_path)                 

    # append ticker data to master
    master_df = master_df.append(feature_df)

# all feature_dfs have the same index, so reset them
#master_df = master_df.reset_index(drop=True)

# write csv
master_df.to_csv(sf.get_csv_path('master'), index = False)
