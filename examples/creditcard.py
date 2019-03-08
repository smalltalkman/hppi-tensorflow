from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
import keras.backend as K
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn import svm
from itertools import product
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import seaborn
# import mxnet as mx

# %matplotlib inline

data = pd.read_csv(r'creditcard.csv')
df = pd.DataFrame(data)
# print(df.head())
# print(df.describe())
#-------------------------------------------------------------------------------
df_corr = df.corr()
# plt.figure(figsize=(15,10))
# seaborn.heatmap(df_corr)
# seaborn.set(font_scale=2)
# plt.title('Heatmap correlation')
# plt.show()
rank = df_corr['Class']
df_rank = pd.DataFrame(rank)
df_rank = np.abs(df_rank).sort_values(by='Class',ascending=False)
df_rank.dropna(inplace=True)
#-------------------------------------------------------------------------------
df_fraud = df[df['Class'] == 1]
# plt.figure(figsize=(15,10))
# plt.scatter(df_fraud['Time'], df_fraud['Amount'])
# plt.title('Scratter plot amount fraud')
# plt.show()
# nb_big_fraud = df_fraud[df_fraud['Amount'] > 1000].shape[0]
# print('There are only '+ str(nb_big_fraud) + ' frauds where the amount was bigger than 1000 over ' + str(df_fraud.shape[0]) + ' frauds')
#-------------------------------------------------------------------------------
mu = df_fraud['Amount'].mean()
sigma = df_fraud['Amount'].std()
# fig, ax = plt.subplots(figsize=(15,10))
# n, bins, patches = ax.hist(df_fraud['Amount'], 30, normed=1)
# y = mlab.normpdf(bins, mu, sigma)
# ax.plot(bins, y, '--')
# ax.set_xlabel('Amount')
# ax.set_ylabel('Probability density')
# ax.set_title('Histogram amount fraud')
# plt.show()
#-------------------------------------------------------------------------------

def model():
  global network_history
  model = Sequential()
  model.add(Dense(64,input_shape=(29,)))
  model.add(Dropout(0.2))
  model.add(Dense(64, kernel_initializer='normal'))
  model.add(Dense(1, activation='sigmoid'))
  
  model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.0001), metrics=['accuracy'])
  
  network_history = model.fit(X_train, y_train, batch_size=128, epochs=300, verbose=0)
  return model

df_train_all = df[0:150000]
df_train_1 = df_train_all[df_train_all['Class'] == 1]
df_train_0 = df_train_all[df_train_all['Class'] == 0]
df_sample = df_train_0.sample(300)
df_train = df_train_1.append(df_sample)
df_train = df_train.sample(frac=1)

df_test_all = df[150000:]
df_test_1 = df_test_all[df_test_all['Class'] == 1]
df_test_0 = df_test_all[df_test_all['Class'] == 0]
df_sample_test = df_test_0.sample(200)
df_test = df_test_1.append(df_sample_test)
df_test = df_test.sample(frac=1)

X_train = df_train.drop(['Time', 'Class'],axis=1)
y_train = df_train['Class']
X_train = np.asarray(X_train)
y_train = np.asarray(y_train)

X_test = df_test.drop(['Time', 'Class'],axis=1)
y_test = df_test['Class']
X_test = np.asarray(X_test)
y_test = np.asarray(y_test)

def model_rank():
  global network_history_rank
  model = Sequential()
  model.add(Dense(32,input_shape=(10,)))
  model.add(Dropout(0.2))
  model.add(Dense(64, kernel_initializer='normal'))
  model.add(Dense(1, activation='sigmoid'))
  
  model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.0001), metrics=['accuracy'])
  
  network_history_rank = model.fit(X_train_rank, y_train, batch_size=128, epochs=300, verbose=0)
  return model

X_train_rank = df_train[df_rank.index[1:11]]
X_train_rank = np.asarray(X_train_rank)

X_test_rank = df_test[df_rank.index[1:11]]
X_test_rank = np.asarray(X_test_rank)

#-------------------------------------------------------------------------------
model = model()
model_rank = model_rank()

#-------------------------------------------------------------------------------
def plot_history(network_history,title='Loss and accuracy (Keras model)'):
  plt.figure(figsize=(15,10))

  plt.subplot(211)
  plt.title(title)
  plt.xlabel('Epochs')
  plt.ylabel('Loss')
  plt.plot(network_history.history['loss'])
  #plt.plot(network_history.history['val_loss'])
  plt.legend(['Training', 'Validation'])

  plt.subplot(212)
  plt.xlabel('Epochs')
  plt.ylabel('Accuracy')
  plt.plot(network_history.history['acc'])
  #plt.plot(network_history.history['val_acc'])
  plt.legend(['Training', 'Validation'], loc='lower right')

  plt.show()

plot_history(network_history)
plot_history(network_history_rank, 'Loss and accuracy with top 10 ranked (Keras model)')

#-------------------------------------------------------------------------------
model.evaluate(X_test, y_test)
model_rank.evaluate(X_test_rank,y_test)

prediction = model.predict(X_test)
prediction_rank = model_rank.predict(X_test_rank)

#-------------------------------------------------------------------------------
plt.figure(figsize=(15,8))
plt.subplot(121)
plt.title('Histogram prediction')
plt.hist(prediction)
plt.subplot(122)
plt.title('Histogram prediction rank')
plt.hist(prediction_rank)
plt.show()

#-------------------------------------------------------------------------------
prediction_bin = prediction > 0.5
prediction_bin = prediction_bin.astype(int)
confusion_matrix(y_test, prediction_bin)

prediction_rank_bin = prediction_rank > 0.5
prediction_rank_bin = prediction_rank_bin.astype(int)
confusion_matrix(y_test, prediction_rank_bin)

#-------------------------------------------------------------------------------
df_test_0_only = df_test_0.sample(200)
X_test_0 = df_test_0_only.drop(['Time','Class'], axis=1)
X_test_0_rank = df_test_0_only[df_rank.index[1:11]]
y_test_0 = df_test_0_only['Class']
X_test_0 = np.asarray(X_test_0)
X_test_0_rank = np.asarray(X_test_0_rank)
y_test_0 = np.asanyarray(y_test_0)

model.evaluate(X_test_0, y_test_0)
model_rank.evaluate(X_test_0_rank,y_test_0)

prediction_0 = model.predict(X_test_0)
prediction_0_bin = prediction_0 > 0.5
prediction_0_bin = prediction_0_bin.astype(int)
confusion_matrix(y_test_0, prediction_0_bin)

prediction_0_rank = model_rank.predict(X_test_0_rank)
prediction_0_bin_rank = prediction_0_rank > 0.5
prediction_0_bin_rank = prediction_0_bin_rank.astype(int)
confusion_matrix(y_test_0, prediction_0_bin_rank)

plt.figure(figsize=(15,8))
plt.subplot(121)
plt.hist(prediction_0)
plt.title('Histogram prediction')

plt.subplot(122)
plt.hist(prediction_0_rank)
plt.title('Histogram prediction rank')
plt.show()

#-------------------------------------------------------------------------------
X_test_all = df_test_all.drop(['Time', 'Class'],axis=1)
X_test_all_rank = df_test_all[df_rank.index[1:11]]
y_test_all = df_test_all['Class']
X_test_all = np.asarray(X_test_all)
X_test_all_rank = np.asarray(X_test_all_rank)
y_test_all = np.asarray(y_test_all)

model.evaluate(X_test_all,y_test_all)
model_rank.evaluate(X_test_all_rank, y_test_all)

prediction_all = model.predict(X_test_all)
prediction_all_rank = model_rank.predict(X_test_all_rank)

plt.figure(figsize=(15,8))
plt.subplot(121)
plt.title('Histogram prediction')
plt.hist(prediction_all)

plt.subplot(122)
plt.title('Histogram prediction rank')
plt.hist(prediction_all_rank)
plt.show()

prediction_all_bin = prediction_all > 0.5
prediction_all_bin = prediction_all_bin.astype(int)
confusion_matrix(y_test_all, prediction_all_bin)

prediction_rank_all_bin = prediction_all_rank > 0.5
prediction_rank_all_bin = prediction_rank_all_bin.astype(int)
confusion_matrix(y_test_all, prediction_rank_all_bin)

#-------------------------------------------------------------------------------
random_forest = RandomForestClassifier(n_estimators=15,)
random_forest.fit(X_train,y_train)

random_forest.score(X_test,y_test)
prediction_RF = random_forest.predict(X_test)
confusion_matrix(y_test, prediction_RF)
random_forest.score(X_test_0,y_test_0)
prediction_RF_0 = random_forest.predict(X_test_0)
confusion_matrix(y_test_0,prediction_RF_0)
random_forest.score(X_test_all,y_test_all)
prediction_RF_all = random_forest.predict(X_test_all)
confusion_matrix(y_test_all, prediction_RF_all)

#-------------------------------------------------------------------------------
AdaBoost = AdaBoostClassifier(learning_rate=0.1)
AdaBoost.fit(X_train, y_train)

AdaBoost.score(X_test, y_test)
prediction_AdaBoost = AdaBoost.predict(X_test)
confusion_matrix(y_test, prediction_AdaBoost)
AdaBoost.score(X_test_0,y_test_0)
prediction_AdaBoost_0 = AdaBoost.predict(X_test_0)
confusion_matrix(y_test_0,prediction_AdaBoost_0)
AdaBoost.score(X_test_all,y_test_all)
prediction_AdaBoost_all = AdaBoost.predict(X_test_all)
confusion_matrix(y_test_all, prediction_AdaBoost_all)

#-------------------------------------------------------------------------------
classifier = svm.SVC(kernel='linear', C=0.01)
classifier.fit(X_train, y_train)

classifier.score(X_test,y_test)
prediction_SVM = classifier.predict(X_test)
confusion_matrix(y_test, prediction_SVM)
classifier.score(X_test_0,y_test_0)
prediction_SVM_0 = classifier.predict(X_test_0)
confusion_matrix(y_test_0,prediction_SVM_0)
classifier.score(X_test_all,y_test_all)
prediction_SVM_all = classifier.predict(X_test_all)
confusion_matrix(y_test_all, prediction_SVM_all)
