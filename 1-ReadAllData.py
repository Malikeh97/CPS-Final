#!/usr/bin/env python
# coding: utf-8

# # Import libraries

# In[1]:


import pandas as pd
from os import listdir
from os.path import isfile, join
import numpy as np


# # Reading the data files

# In[2]:


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

# In[3]:

df_tag_summary = df.groupby(['uuid']).count()
df_tag_summary[:10]


# In[4]:

valid_tags = ['d6:fb:b2:5e:83:c5']
data = df[df['uuid'].isin(valid_tags)]



# # Changing 9.9m to 10.0m

# In[6]:


data.columns = ['uuid', 'distance', 'rssi']
# data = data.drop_duplicates() #why?

#data['Distance'] = data['Distance'].apply(lambda x: 0.03 if x == 0.0 else x)


# # Saving data in a file

# In[7]:

print(data)
data.to_csv('data.csv', index = False, header = data.columns)
