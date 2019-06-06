# # Import libraries and loading data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# read csv file
data = pd.read_csv('data.csv')


# # Selecting a tag, gateway, and TxPower to work on

TAG = 'd6:fb:b2:5e:83:c5'
GATEWAY = 'RaspberryPi'
df = data[(data['uuid'] == TAG)]

#Reset the index of the DataFrame, and use the default one instead. If the DataFrame has a MultiIndex, this method can remove one or more levels.
df = df.reset_index()


# # Visualizing RSSI vs Distance

pd.options.mode.chained_assignment = None
plt.figure(figsize=(16,8))
plt.title('RSSI plot for Tag: ' + TAG + ' Gateway: ' + GATEWAY )

columns =['distance']
df[columns] = df[df[columns] > -120][columns]
df.dropna()

for distance in df['distance'].unique():
    df_view = df[df['distance'] == distance]
    ax = df_view['rssi'].plot(label = str(distance) + 'm')

plt.legend(loc='upper left')
plt.grid(True)
plt.show()


# In[5]:


ax = df[['distance', 'rssi']].boxplot(by='distance', figsize=(16,8))
plt.show()
