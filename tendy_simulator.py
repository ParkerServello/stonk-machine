import stonk_functions as sf
import pandas as pd
import datetime as dt

# select metric to determine who to buy
metric = 'macd_diff_short'

# date range
end_date = '2020-08-10'
lookback_days = 10

# read master data
master_df = pd.read_csv(sf.get_csv_path('master'))

# copy master
staging_master_df = master_df.copy()

# apply a date range
start_date = (dt.datetime.strptime(end_date, '%Y-%m-%d') - dt.timedelta(lookback_days)).strftime('%Y-%m-%d')
staging_master_df = staging_master_df[(staging_master_df['date'] >= start_date) & (staging_master_df['date'] <= end_date)]


for n in range(1,15):
    
    # find the best MACDs for each day
    best_macd_df = staging_master_df.loc[staging_master_df.groupby('date')[metric].nlargest(n).reset_index()['level_1']]
    
    # find the average oto for each day
    average_gains_df = best_macd_df.groupby('date')['next_oto'].mean()
    
    # convert percentage change to multiplier
    tendy = (average_gains_df / 100 + 1).product()
    
    print(f'n: {n} : {tendy}')

(average_gains_df / 100 + 1).mean()

