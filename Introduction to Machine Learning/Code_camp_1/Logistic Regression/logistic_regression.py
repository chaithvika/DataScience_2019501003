# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.impute import KNNImputer
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.neural_network import MLPClassifier

path = """C:/Users/kittu/Documents/DS_Specialization/DataScience_2019501003/Introduction to Machine Learning/Code_camp_1/Logistic Regression/"""
train = path + "train.csv"
test = path + "test.csv"

trainx_df = pd.read_csv(train)
test_df = pd.read_csv(test)

trainy_df = trainx_df['responded']
trainx_df.drop('responded', axis=1, inplace=True)

sample_size = len(trainx_df)
columns_with_null_values = []
for col in trainx_df.columns:
    if trainx_df[col].isnull().sum():
        columns_with_null_values.append([col, float(trainx_df[col].isnull().sum()) / float(sample_size)])        
columns_to_drop = [x for (x,y) in columns_with_null_values if y>0.25]
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

imputer = KNNImputer(n_neighbors = 5)
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
# print(test_df.shape)

le = preprocessing.LabelEncoder()
trainy_df=le.fit_transform(trainy_df)

pca = PCA().fit(trainx_df)
itemindex = np.where(np.cumsum(pca.explained_variance_ratio_)>0.9999)
print('np.cumsum(pca.explained_variance_ratio_)',      np.cumsum(pca.explained_variance_ratio_))
#Plotting the Cumulative Summation of the Explained Variance
plt.figure(np.cumsum(pca.explained_variance_ratio_)[0])
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('Number of Components')
plt.ylabel('Variance (%)') #for each component
plt.title('Principal Components Explained Variance')
plt.show()
pca_std = PCA(n_components=itemindex[0][0]).fit(trainx_df)
trainx_df = pca_std.transform(trainx_df)
test_df = pca_std.transform(test_df)

# print(trainx_df.shape)
# print(test_df.shape)

X_train, X_test, y_train, y_test = train_test_split(trainx_df, trainy_df, test_size=0.3, random_state=42)

print("Results for Logistic Regression")


logreg=LogisticRegression(class_weight="balanced",C=0.00001,max_iter=1000000)
logreg.fit(X_train, y_train)

# getScores

yprobs= logreg.predict_log_proba(X_test)
yprobs=yprobs[:,1]
ras=roc_auc_score(y_test,yprobs,average = 'weighted')
print(ras)
yhat = logreg.predict(X_test)

TP, TN, FP, FN =0,0,0,0
for i in range(len(yhat)):
    if yhat[i]==0:
        if y_test[i]==0:
            TN+=1
        else:
            FN+=1
    else:
        if y_test[i]==1:
            TP+=1
        else:
            FP+=1
print(classification_report(y_test,yhat))
print(classification_report(y_test,yhat,output_dict=True)['1']['precision'], classification_report(y_test,yhat,output_dict=True)['1']['recall'])
fpr, tpr, threshold = roc_curve(y_test, yprobs)
roc_auc = auc(fpr, tpr)

plt.title('Receiver Operating Characteristic')
plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()
print([TP, TN,FP,FN,TP/(TP+FN), TN/(TN+FP)])

print("Results for SVM Classifier")

svcmodel=SVC(C=0.5,degree=2,kernel='poly')
svcmodel.fit(X_train, y_train)

# getScoresForSVC

yhat = svcmodel.predict(X_test)
#pd.DataFrame(yhat).to_csv(model)
TP, TN, FP, FN =0,0,0,0
for i in range(len(yhat)):
    if yhat[i]==0:
        if y_test[i]==0:
            TN+=1
        else:
            FN+=1
    else:
        if y_test[i]==1:
            TP+=1
        else:
            FP+=1
print(classification_report(y_test,yhat))
print(classification_report(y_test,yhat,output_dict=True)['1']['precision'], classification_report(y_test,yhat,output_dict=True)['1']['recall'])
print([TP, TN,FP,FN,TP/(TP+FN), TN/(TN+FP)])

print("Results for Back Propagation Classifier")
nn_bp_model = MLPClassifier(solver='lbfgs', alpha=0.01, hidden_layer_sizes=(7, ), random_state=1, max_iter=10000)
nn_bp_model.fit(X_train, y_train)
    
# getScores for nn_bp_model

yprobs= nn_bp_model.predict_log_proba(X_test)
yprobs=yprobs[:,1]
ras=roc_auc_score(y_test,yprobs,average = 'weighted')
print(ras)
yhat = nn_bp_model.predict(X_test)
#pd.DataFrame(yhat).to_csv(model)
TP, TN, FP, FN =0,0,0,0
for i in range(len(yhat)):
    if yhat[i]==0:
        if y_test[i]==0:
            TN+=1
        else:
            FN+=1
    else:
        if y_test[i]==1:
            TP+=1
        else:
            FP+=1
print(classification_report(y_test,yhat))
print(classification_report(y_test,yhat,output_dict=True)['1']['precision'], classification_report(y_test,yhat,output_dict=True)['1']['recall'])
fpr, tpr, threshold = roc_curve(y_test, yprobs)
roc_auc = auc(fpr, tpr)

plt.title('Receiver Operating Characteristic')
plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()
print([TP, TN,FP,FN,TP/(TP+FN), TN/(TN+FP)])