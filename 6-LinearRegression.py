#!/usr/bin/env python
# coding: utf-8

# # Import libraries and loading data
# 

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures

# read csv file
df = pd.read_csv('data_spikes_removed.csv')


# # Feature Extraction

# ## Rolling Average

# In[2]:


# The conclusion of the rolling average file
window_size = 5 
column_name = 'Rolling' + str(window_size)
df[column_name] = np.nan
    
for dist in df['Distance'].unique():
    df.loc[df['Distance'] == dist, column_name] =  df[df['Distance'] == dist]['RSSI'].rolling(window_size).mean()
    
df = df[df[column_name].notnull()]


# In[3]:


# create training and testing vars
X = df[['RSSI', column_name]]
y = df['Distance'].values.reshape(-1, 1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

lm = linear_model.LinearRegression()
model = lm.fit(X_train, y_train)
predictions = lm.predict(X_test)


# In[8]:


poly = PolynomialFeatures(degree=4)
X_train_ = poly.fit_transform(X_train)
X_test_ = poly.fit_transform(X_test)

lm = linear_model.LinearRegression()
model = lm.fit(X_train_, y_train)
predictions = lm.predict(X_test_)


# In[9]:


plt.figure(figsize=(16,8))
plt.scatter(y_test, predictions)
plt.grid(True)
plt.xlabel('True Values')
plt.ylabel('Predictions')
print('Score:', model.score(X_test_, y_test))


# In[32]:


np.round(predictions - y_test, 2).sum()


# In[ ]:


from sklearn.model_selection import KFold # import KFold
X = np.array([[1, 2], [3, 4], [1, 2], [3, 4]]) # create an array
y = np.array([1, 2, 3, 4]) # Create another array
kf = KFold(n_splits = 2) # Define the split - into 2 folds 
kf.get_n_splits(X) # returns the number of splitting iterations in the cross-validator
print(kf) 
KFold(n_splits=2, random_state=None, shuffle=False)

