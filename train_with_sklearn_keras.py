
SEED = 7

import numpy as np
np.random.seed(SEED)

from keras.models import Sequential
from keras.layers import Dense

def create_model(input_dim, hidden_units, kernel_initializer, activation, loss, optimizer, metrics=None):
  model = Sequential()

  if isinstance(hidden_units, str):
    hidden_units = list(map(lambda x:int(x), hidden_units.split('x')))

  if metrics is None:
    metrics = ['accuracy']

  for index, hidden_unit in enumerate(hidden_units):
    if index == 0:
      model.add(Dense(hidden_unit, kernel_initializer=kernel_initializer, activation=activation, input_dim=input_dim))
    else:
      model.add(Dense(hidden_unit, kernel_initializer=kernel_initializer, activation=activation))

  model.add(Dense(1, kernel_initializer=kernel_initializer, activation='sigmoid'))

  model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
  return model

from keras.wrappers.scikit_learn import KerasClassifier

model = KerasClassifier(build_fn=create_model
                       ,input_dim=686
                       ,hidden_units='12x8'
                       ,kernel_initializer='uniform'
                       ,activation='relu'
                       ,loss='binary_crossentropy'
                       ,optimizer='adam'
                       ,epochs=50
                       ,batch_size=128
                       )

import hppi

hppids = hppi.read_data_sets("data/02-ct-bin", one_hot=False)
X = hppids.datas
Y = hppids.labels

from sklearn.model_selection import StratifiedKFold, cross_val_score

kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=SEED)
results = cross_val_score(model, X, Y, cv=kfold)

print(np.average(results))

# if __name__ == "__main__":
  # create_model(686, [12, 8], 'uniform', 'relu', 'binary_crossentropy', 'adam', ['accuracy'])
