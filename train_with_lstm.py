
SEED = 7

import numpy
numpy.random.seed(SEED)

AMINO_ACIDS='ACDEFGHIKLMNPQRSTVWY'
AMINO_ACID_MAP={ AMINO_ACID : INDEX+1 for (INDEX, AMINO_ACID) in enumerate(AMINO_ACIDS) }
AMINO_ACID_DIM=len(AMINO_ACIDS)+1

def to_int_list(chars):
  return [ AMINO_ACID_MAP[char] for char in chars ]

import pandas

positive_datas = pandas.read_csv("data/01-flat/Supp-A-36630-HPRD-positive-interaction.txt", header=None)
positive_datas['seq_pair'] = (positive_datas[0]+positive_datas[1]).map(to_int_list)
positive_datas['class'] = 1

negative_datas = pandas.read_csv("data/01-flat/Supp-B-36480-HPRD-negative-interaction.txt", header=None)
negative_datas['seq_pair'] = (negative_datas[0]+negative_datas[1]).map(to_int_list)
negative_datas['class'] = 0

all_datas = pandas.concat([positive_datas, negative_datas])

X = all_datas['seq_pair']
y = all_datas['class']

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=SEED)

from keras.preprocessing import sequence

max_length = 1000
X_train  = sequence.pad_sequences(X_train,  maxlen=max_length)
X_test   = sequence.pad_sequences(X_test,   maxlen=max_length)

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding

emb_vecor_length = 32
model = Sequential()
model.add(Embedding(AMINO_ACID_DIM, emb_vecor_length, input_length=max_length))
model.add(LSTM(100))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit(X_train, y_train, epochs=3, batch_size=64)

scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))
