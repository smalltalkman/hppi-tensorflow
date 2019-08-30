
from keras.models import Sequential
from keras.layers import Dense

def create_model():
  model = Sequential()
  model.add(Dense(12, input_dim=8, kernel_initializer='uniform', activation='relu'))
  model.add(Dense(8, kernel_initializer='uniform', activation='relu'))
  model.add(Dense(1, kernel_initializer='uniform', activation='sigmoid'))
  model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
  return model

from keras.wrappers.scikit_learn import KerasClassifier

model = KerasClassifier(build_fn=create_model, epochs=150, batch_size=10)

import numpy as np
seed = 7
np.random.seed(seed)

dataset = np.loadtxt('pima-indians-diabetes.csv', delimiter=',')
X = dataset[:, 0:8]
Y = dataset[:,   8]

from sklearn.cross_validation import StratifiedKFold, cross_val_score

kfold = StratifiedKFold(Y, n_folds=10, shuffle=True, random_state=seed)
results = cross_val_score(model, X, Y, cv=kfold)

print(np.average(results))
