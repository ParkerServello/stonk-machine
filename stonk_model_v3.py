import stonk_functions as  sf
import pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import sklearn as sk
import datetime as dt
import numpy as np
from sklearn import preprocessing

today = (dt.datetime.now() - dt.timedelta(365)).strftime('%Y-%m-%d')

# read master data
master_df = pd.read_csv(sf.get_csv_path('master'))

# drop excessively null columns
null_cols = ['trend_psar_up', 'trend_psar_down']
master_df = master_df.drop(null_cols, axis=1)

# copy master
input_df = master_df.copy()

# copy master and remove na
input_df = input_df.dropna()

# split input
test_input_df = input_df[input_df['date'] > today]
input_df = input_df[input_df['date'] < today]

# remove last trading day from test_input_df since we don't know the next oto
test_input_df = test_input_df[test_input_df['date'] != test_input_df['date'].max()]

# choose features
feature_set = input_df.columns.difference(['date','open','ticker','next_oto'])

# choose input columns, reshape if we only have 1
X = input_df[feature_set]

'''
# normalize some columns
X_array = X.values #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
X_scaled = min_max_scaler.fit_transform(X_array)
X = pd.DataFrame(X_scaled)
'''

# buy threshold
c = .1

# create target
y = pd.Series([0 if target > c else 1 for target in input_df['next_oto']])

# see distribution
y.value_counts()

# train test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.1, random_state=42)

'''
# intialize model
reg = linear_model.LogisticRegression(solver = 'lbfgs')

# train model
reg.fit(X_train, y_train)

# performance metrics
reg.score(X_test, y_test)
scores = sk.model_selection.cross_val_score(reg, X, y, cv=5)
print("Accuracy: %0.2f (+/- %0.2f) \n" % (scores.mean(), scores.std() * 2))
'''

# intialize model
est = sm.Logit(np.asarray(y_train), np.asarray(X_train))

# train model
est = est.fit()

# results
#print(est.summary())

# columns names with numbers
list(zip(range(1,len(X.columns)),X.columns))

# simulating
y_pred = pd.Series(est.predict(np.array(test_input_df[feature_set]))).rename('prediction')
uh = y_pred.value_counts()

# when to buy what
winners = pd.concat([test_input_df.reset_index(), y_pred], axis=1)
winners = winners[winners['prediction']==1][['date','ticker','next_oto']]

transaction_counts = winners.groupby('date')['next_oto'].count()

average_gains_df = winners.groupby('date')['next_oto'].mean()
print(f'tendies: {(average_gains_df / 100 + 1).product()}')













