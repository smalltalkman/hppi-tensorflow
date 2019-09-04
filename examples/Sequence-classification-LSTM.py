
import numpy
numpy.random.seed(7)

from keras.datasets import imdb
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding

# load the dataset but only keep the top n words, zero the rest
top_w = 5000
(X_tr, y_tr), (X_tst, y_tst) = imdb.load_data(num_words=top_w)

# truncate and pad input sequences
max_review_length = 500
X_tr  = sequence.pad_sequences(X_tr,  maxlen=max_review_length)
X_tst = sequence.pad_sequences(X_tst, maxlen=max_review_length)

# create the model
emb_vecor_length = 32
modelClass = Sequential()
modelClass.add(Embedding(top_w, emb_vecor_length, input_length=max_review_length))
modelClass.add(LSTM(100))
modelClass.add(Dense(1, activation='sigmoid'))
modelClass.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(modelClass.summary())
modelClass.fit(X_tr, y_tr, epochs=3, batch_size=64)

# Final evaluation of the model
scores = modelClass.evaluate(X_tst, y_tst, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))
