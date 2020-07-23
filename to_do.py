import pandas as pd
import stonk_functions as sf
from ta import add_all_ta_features

data = pd.read_csv(sf.get_csv_path('processed', 'MSFT'))

#  buy if oto gain is greater than the threshold
buy_threshold = 0
data['buy'] = False
data.loc[data['oto'] > buy_threshold, 'buy'] = True





#https://github.com/bukosabino/ta for feature engineering
#https://github.com/FeatureLabs/featuretools











# where we'll save the last row for each ticker (today) to predict tomorrow's oto
inputs_df = pd.DataFrame()

# save last row for today's oto prediction and remove it from data
ticker_input = data.iloc[-1,:-2]
data = data[:-1]

# change ticker_input index to ticker and append to input csv
ticker_input = ticker_input.rename(ticker)
inputs_df = inputs_df.append(inputs_df)
    
# save model inputs
inputs_df.to_csv(sf.get_csv_path('input'))