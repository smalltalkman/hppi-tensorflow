
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

SEED = 7

import numpy as np
np.random.seed(SEED)

from keras.models import Sequential
from keras.layers import Dense, Dropout

def create_model(input_dim, hidden_units, kernel_initializer, activation, dropout_rate, loss, optimizer, metrics):
  model = Sequential()

  for index, hidden_unit in enumerate(hidden_units):
    if index == 0:
      model.add(Dense(hidden_unit, kernel_initializer=kernel_initializer, activation=activation, input_dim=input_dim))
    else:
      model.add(Dense(hidden_unit, kernel_initializer=kernel_initializer, activation=activation))
    model.add(Dropout(dropout_rate))

  model.add(Dense(1, kernel_initializer=kernel_initializer, activation='sigmoid'))

  model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
  return model

import hppi, pandas

def load_hppids(dir):
  hppids = hppi.read_data_sets(dir, one_hot=False)
  X = hppids.datas
  Y = hppids.labels
  print('Success to load ', dir, ', Shape: ', X.shape)
  
  return pandas.DataFrame(X), pandas.DataFrame(Y)

def main():

  ct_X, ct_Y = load_hppids("data/02-ct-bin")
  ac_X, ac_Y = load_hppids("data/03-ac-bin")
  ld_X, ld_Y = load_hppids("data/04-ld-bin")

  X = pandas.concat([ct_X, ac_X, ld_X])
  X.fillna(0, inplace=True)
  # X = X.drop_duplicates()

  Y = pandas.concat([ct_Y, ac_Y, ld_Y])

  # from sklearn.model_selection import train_test_split

  # X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.4, random_state=SEED)

  from keras.wrappers.scikit_learn import KerasClassifier

  ct_model = KerasClassifier(build_fn=create_model
                            ,input_dim=1260 #686
                            ,hidden_units=[256, 256, 256]
                            ,kernel_initializer='uniform'
                            ,activation='relu'
                            ,dropout_rate=0.4
                            ,loss='binary_crossentropy'
                            ,optimizer='adam'
                            ,metrics=['accuracy']
                            ,epochs=50
                            ,batch_size=128
                            )

  ac_model = KerasClassifier(build_fn=create_model
                            ,input_dim=1260 #420
                            ,hidden_units=[256, 256, 256]
                            ,kernel_initializer='uniform'
                            ,activation='relu'
                            ,dropout_rate=0.7
                            ,loss='binary_crossentropy'
                            ,optimizer='adam'
                            ,metrics=['accuracy']
                            ,epochs=50
                            ,batch_size=128
                            )

  ld_model = KerasClassifier(build_fn=create_model
                            ,input_dim=1260 #1260
                            ,hidden_units=[256, 128, 64, 32]
                            ,kernel_initializer='uniform'
                            ,activation='relu'
                            ,dropout_rate=0.1
                            ,loss='binary_crossentropy'
                            ,optimizer='adam'
                            ,metrics=['accuracy']
                            ,epochs=50
                            ,batch_size=128
                            )

  from sklearn.ensemble import VotingClassifier

  model = VotingClassifier( estimators=[("ct", ct_model), ("ac", ac_model), ("ld", ld_model)], voting="hard" ) # soft

  from sklearn.model_selection import StratifiedKFold, cross_val_score

  kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=SEED)
  results = cross_val_score(model, X, Y, cv=kfold)
  print(np.average(results))

if __name__ == "__main__":
  main()
