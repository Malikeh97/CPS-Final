# # Import libraries

import pandas as pd
from os import listdir
from os.path import isfile, join
import numpy as np


# # Reading the data files
data_path = 'data/'
all_data = []

for file in listdir(data_path):
        file_path = data_path + '/' + file
        df = pd.read_csv(file_path)
        all_data.append(df)

df = pd.concat(all_data)



# # Filtering unknown tags
# There may some unknow BLE devices which have been detected by our gateways and we should filter them.
# Also, we have 2 data points for each tag: RSSI (Type=1) and TxPower (Type=2)

df_tag_summary = df.groupby(['uuid']).count()
df_tag_summary[:10]


valid_tags = ['d6:fb:b2:5e:83:c5']
data = df[df['uuid'].isin(valid_tags)]

data.columns = ['uuid', 'distance', 'rssi']


# # Saving data in a file

print(data)
data.to_csv('data.csv', index = False, header = data.columns)
