
# # Import libraries and loading data
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

# The conclusion of the rolling average file
window_size = 15
column_name = 'Rolling' + str(window_size)
df[column_name] = np.nan
print('1: ',df)
for dist in df['distance'].unique():
    df.loc[df['distance'] == dist, column_name] =  df[df['distance'] == dist]['rssi'].rolling(window_size).mean()

df = df[df[column_name].notnull()]
print('2: ', df)

# create training and testing vars
X = df[['rssi', column_name]]
y = df['distance'].values.reshape(-1, 1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

lm = linear_model.LinearRegression()
model = lm.fit(X_train, y_train)
predictions = lm.predict(X_test)


poly = PolynomialFeatures(degree=4)
X_train_ = poly.fit_transform(X_train)
X_test_ = poly.fit_transform(X_test)

lm = linear_model.LinearRegression()
model = lm.fit(X_train_, y_train)
predictions = lm.predict(X_test_)


plt.figure(figsize=(16,8))
plt.scatter(y_test, predictions)
plt.grid(True)
plt.xlabel('True Values')
plt.ylabel('Predictions')
print('Score:', model.score(X_test_, y_test))



np.round(predictions - y_test, 2).sum()


from sklearn.model_selection import KFold # import KFold
X = np.array([[1, 2], [3, 4], [1, 2], [3, 4]]) # create an array
y = np.array([1, 2, 3, 4]) # Create another array
kf = KFold(n_splits = 2) # Define the split - into 2 folds
kf.get_n_splits(X) # returns the number of splitting iterations in the cross-validator
print(kf)
KFold(n_splits=2, random_state=None, shuffle=False)
