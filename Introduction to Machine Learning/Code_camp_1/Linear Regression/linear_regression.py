# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.impute import KNNImputer
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error as mserr
from sklearn.decomposition import PCA
from sklearn.model_selection import RandomizedSearchCV
from sklearn.kernel_ridge import KernelRidge

path = """C:/Users/kittu/Documents/DS_Specialization/DataScience_2019501003/Introduction to Machine Learning/Code_camp_1/Linear Regression/"""


train = path + "train.csv"
test = path + "test.csv"

trainx_df = pd.read_csv(train, index_col = 'Id')
test_df = pd.read_csv(test, index_col = 'Id')

trainy_df = trainx_df['SalePrice']
trainx_df.drop('SalePrice', axis=1, inplace=True)

sample_size = len(trainx_df)
columns_with_null_values = []
for col in trainx_df.columns:
    if trainx_df[col].isnull().sum():
        columns_with_null_values.append([col, float(trainx_df[col].isnull().sum()) / float(sample_size)])        
columns_to_drop = [x for (x,y) in columns_with_null_values if y>0.3]
trainx_df.drop(columns_to_drop, axis = 1, inplace = True)
test_df.drop(columns_to_drop, axis = 1, inplace = True)

categorical_columns = [col for col in trainx_df.columns if trainx_df[col].dtype == object]
ordinal_columns = [col for col in trainx_df.columns if col not in categorical_columns]

dummy_row = list()
for col in trainx_df.columns:
    if col in categorical_columns:
        dummy_row.append('dummy')
    else:
        dummy_row.append("")

new_row = pd.DataFrame([dummy_row], columns = trainx_df.columns)
trainx_df = pd.concat([trainx_df, new_row], axis = 0, ignore_index = True)
test_df = pd.concat([test_df, new_row], axis = 0, ignore_index = True)

for col in categorical_columns:
    trainx_df[col].fillna(value = 'dummy', inplace = True)
    test_df[col].fillna(value = 'dummy', inplace = True)

enc = OneHotEncoder(drop = 'first', sparse = False)
enc.fit(trainx_df[categorical_columns])
trainx_enc = pd.DataFrame(enc.transform(trainx_df[categorical_columns]))
test_enc = pd.DataFrame(enc.transform(test_df[categorical_columns]))
# print(trainx_df.shape)
# print(test_df.shape)

trainx_enc.columns = enc.get_feature_names(categorical_columns)
test_enc.columns = enc.get_feature_names(categorical_columns)
trainx_df = pd.concat([trainx_df[ordinal_columns], trainx_enc], axis = 1, ignore_index = True)
test_df = pd.concat([test_df[ordinal_columns], test_enc], axis = 1, ignore_index = True)

trainx_df.drop(trainx_df.tail(1).index, inplace = True)
test_df.drop(test_df.tail(1).index, inplace = True)
# print(trainx_df.shape)

imputer = KNNImputer(n_neighbors = 2)
imputer.fit(trainx_df)
trainx_df_filled = imputer.transform(trainx_df)
trainx_df_filled = pd.DataFrame(trainx_df_filled, columns = trainx_df.columns)

test_df_filled = imputer.transform(test_df)
test_df_filled = pd.DataFrame(test_df_filled, columns = test_df.columns)
test_df_filled.reset_index(drop = True, inplace = True)

# print(trainx_df_filled.isnull().sum())

scaler = preprocessing.StandardScaler().fit(trainx_df)
trainx_df=scaler.transform(trainx_df_filled)
test_df=scaler.transform(test_df_filled)

# print(trainx_df.shape)
# print(trainx_df_filled.shape)

X_train, X_test, y_train, y_test = train_test_split(trainx_df, trainy_df.values.ravel(), test_size=0.3, random_state=42)

LRModel = LinearRegression().fit(X_train, y_train)

score_train = []
score_test = []
mse_train = []
mse_test = []
alpha = []
alpha_start = 2
alpha_end = 146
jumps = 10
for sigma in np.linspace(alpha_start, alpha_end, jumps):
    alpha.append(sigma)
    Ridge_model = Ridge(alpha=sigma, tol=0.01).fit(X_train, y_train)
    score_train.append(round(Ridge_model.score(X_train, y_train), 10))
    score_test.append(round(Ridge_model.score(X_test, y_test), 10))
    mse_train.append(round(mserr(y_train,Ridge_model.predict(X_train)), 4))
    mse_test.append(round(mserr(y_test,Ridge_model.predict(X_test)), 4))
print(alpha,'\n', score_train, '\n', score_test,'\n', mse_train, '\n', mse_test) 

Ridge_model = Ridge(alpha = 146,tol = 0.01).fit(X_train, y_train)
testpred = pd.DataFrame(Ridge_model.predict(test_df))
testpred.to_csv("test_pred.csv")

plt.figure(1)
plt.plot(alpha, score_train, 'g--', label="train_score")
plt.plot(alpha, score_test, 'r-o', label="test_score")
plt.xlabel='Alpha'
plt.legend()
plt.figure(2)
plt.plot(alpha, mse_train, 'y--', label="train_mse")
plt.plot(alpha, mse_test, 'c-o', label="test_mse")
plt.xlabel='Alpha'
plt.legend()
plt.show() 
