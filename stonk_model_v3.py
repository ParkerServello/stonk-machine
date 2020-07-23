#https://github.com/bukosabino/ta

import stonk_functions as  sf
import pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
import numpy as np
from ta import add_all_ta_features
from ta.utils import dropna


processed_path = sf.get_csv_path('processed', 'MSFT')
data = pd.read_csv(processed_path)
