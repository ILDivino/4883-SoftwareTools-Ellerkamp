from datetime import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy as np
import pandas as pd

df = pd.read_csv('CHO/CHO_2020.csv', # read the data into a pandas dataframe
                 parse_dates=['date'], # parse and index the columns by the date
                 index_col= ['date'])

# these columns are empty, drop them from the dataframe
df = df.drop(['record_avg_temp', 'record_precipitation'], axis=1)

# replace any other empty cells with NaNs
df = df.replace('--',np.nan)

# due to hardware (i.e., weather station) failures, a few
# days have all data set as NaNs, drop these rows
df = df.dropna(subset=['actual_high_temp'])

# handles converting strings containing negative numbers (i.e., '-') to floats
df['record_low_temp'] = pd.to_numeric(df['record_low_temp'], errors='coerce')

# due to hardware (i.e., weather station) failures, a few days have
# Actual Low Temp set to 0, in the middle of summer, replace with NaN
df.loc[df['actual_low_temp'] == 0] = np.nan
# interpolate over NaNs in Actual Low Temp
df['actual_low_temp'] = df['actual_low_temp'].interpolate()

# add month column
df['month'] = df.index.month
# calculate mean, median, and total temperatures and precipitation for each month
month_avg = df.groupby('month').agg(['mean','median','sum'])

fig, ax = plt.subplots(2, 1, figsize=(10, 8))

# first subplot
# plot monthly average Actual Avg Temp and average Historical Avg
ax[0].plot(month_avg.index, month_avg['actual_avg_temp']['mean'], color='dodgerblue', linewidth=3.0, label='Actual Avg.')
ax[0].plot(month_avg.index, month_avg['histavg_avg_temp']['mean'], color='salmon', linewidth=3.0, ls='--', label='Historical Avg.')

# second subplot
# plot monthly total Actual Precipitation and total Historical Avg Precipitation
ax[1].plot(month_avg.index, month_avg['actual_precip']['sum'], color='seagreen', linewidth=3.0, label='Actual Total')
ax[1].plot(month_avg.index, month_avg['histavg_precip']['sum'], color='darkorange', linewidth=3.0, ls='--', label='Historical Total')

# set xtick labels as month names on both subplots
ax[0].set_xticks(range(1, 13, 1)) 
ax[0].set_xticklabels([datetime(year=2016, month=x, day=1).strftime('%b')
                                     for x in range(1, 13, 1)], fontsize=12)

ax[1].set_xticks(range(1, 13, 1)) 
ax[1].set_xticklabels([datetime(year=2016, month=x, day=1).strftime('%b')
                                     for x in range(1, 13, 1)], fontsize=12)
# set axis label
ax[1].set_xlabel(r'Month', fontsize=14)

# set ylim and ytick labels on first subplot with degree format
ax[0].set_ylim(10,100)  
ax[0].set_yticks(range(0, 111, 10))
ax[0].set_yticklabels([r'{}$^\circ$'.format(x)
                                     for x in range(0, 111, 10)], fontsize=12)
# set axis label
ax[0].set_ylabel(r'Temperature ($^\circ$F)', fontsize=14)

# set ylim and axis label on second subplot
ax[1].set_ylim(0,7)
ax[1].set_ylabel(r'Precipitation (inches)', fontsize=14)

# include legends
ax[0].legend()
ax[1].legend()

# plot title
plt.suptitle('Charlottesville, VA (CHO), 2020\n', fontsize=16)

# formatting for nice saved figure
plt.tight_layout()

# save figure to same directory as csv file
plt.savefig('CHO/CHO_avgtemp_totalprecip.pdf', dpi=300)