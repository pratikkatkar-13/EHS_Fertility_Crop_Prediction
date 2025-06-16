import tensorflow as tf
from tensorflow import keras
import cv2
import numpy as np
import pandas as pd

data=pd.read_csv('Crop.csv')
print(data)

from sklearn.preprocessing import LabelEncoder

label1 =data.iloc[:,7]

label_encoder = LabelEncoder()

encoded_crops = label_encoder.fit_transform(label1)
print(encoded_crops)

X=data.iloc[:,0:7]
X
y=encoded_crops

from sklearn.model_selection import train_test_split
X_train1, X_test, y_train1, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

X_train, X_val, y_train, y_val = train_test_split(X_train1, y_train1, test_size = 0.2, random_state=2022)
print(X_train.shape, X_val.shape)
RF = RandomForestClassifier()
RF.fit(X_train , y_train)
RF_accuracy = RF.score(X_test,y_test)
print('Training Accuracy : ',metrics.accuracy_score(y_train1, RF.predict(X_train1))*100)
print('Validation Accuracy : ',metrics.accuracy_score(y_val, RF.predict(X_val))*100)
print(RF_accuracy)