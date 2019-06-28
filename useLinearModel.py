import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
import pickle

loaded_model = pickle.load(open('finalizedModel.sav','rb'))

X = [[-85, -85]]
poly = PolynomialFeatures(degree=4)
X = poly.fit_transform(X)
result = loaded_model.predict(X)
print(result)
