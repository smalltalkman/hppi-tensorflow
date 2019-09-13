
SEED = 7

import numpy
numpy.random.seed(SEED)

AMINO_ACIDS='*-ACDEFGHIKLMNPQRSTVWY'
AMINO_ACID_MAP={ AMINO_ACID : INDEX for (INDEX, AMINO_ACID) in enumerate(AMINO_ACIDS) }
AMINO_ACID_DIM=len(AMINO_ACIDS)

def to_int_list(chars):
  return [ AMINO_ACID_MAP[char] for char in chars ]

import pandas

max_length = 1000

positive_datas = pandas.read_csv("data/01-flat/Supp-A-36630-HPRD-positive-interaction.txt", header=None)
positive_datas['seq_pair'] = (positive_datas[0]+'-'+positive_datas[1]).map(to_int_list)
positive_datas['class'] = 1
positive_datas = positive_datas[positive_datas['seq_pair'].map(len)<=max_length]

negative_datas = pandas.read_csv("data/01-flat/Supp-B-36480-HPRD-negative-interaction.txt", header=None)
negative_datas['seq_pair'] = (negative_datas[0]+'-'+negative_datas[1]).map(to_int_list)
negative_datas['class'] = 0
negative_datas = negative_datas[negative_datas['seq_pair'].map(len)<=max_length]

all_datas = pandas.concat([positive_datas, negative_datas])

X = all_datas['seq_pair']
y = all_datas['class']

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED)

from keras.preprocessing import sequence

X_train  = sequence.pad_sequences(X_train,  maxlen=max_length)
X_test   = sequence.pad_sequences(X_test,   maxlen=max_length)

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding

emb_vecor_length = 256
model = Sequential()
model.add(Embedding(AMINO_ACID_DIM, emb_vecor_length, mask_zero=True, input_length=max_length))
model.add(LSTM(100))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())

history = model.fit(X_train, y_train, shuffle=True, validation_split=0.25, epochs=20, batch_size=64)

scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))

import json
with open('train_with_sklearn_keras_lstm.json', 'w') as file:
  json.dump(history.history, file)
