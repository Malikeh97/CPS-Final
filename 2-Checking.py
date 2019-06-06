# # Import libraries and loading data
import gc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


gc.enable()

# read csv file
data = pd.read_csv('data.csv')

# # Checking collected data

#RSSI Mean
df_gateway_summary = data.groupby(['distance']).mean()#.sort_values(ascending=False)
df_gateway_summary.plot(kind='bar', figsize=(16,8), grid = True, title = 'RSSI Mean')
plt.show()
