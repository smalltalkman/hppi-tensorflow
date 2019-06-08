from keras import regularizers
from keras.layers import Input, Dense
from keras.models import Model

def create_autoencoder(input_dim, encoding_dim):
  input   = Input(shape=(input_dim,))
  encoded = Dense(encoding_dim, activation='relu', activity_regularizer=regularizers.l1(10e-5))(input)
  decoded = Dense(input_dim, activation='sigmoid')(encoded)

  autoencoder = Model(input, decoded)
  encoder     = Model(input, encoded)

  encoded_input = Input(shape=(encoding_dim,))
  decoder_layer = autoencoder.layers[-1]
  decoder       = Model(encoded_input, decoder_layer(encoded_input))

  autoencoder.summary()
  encoder.summary()
  decoder.summary()

  return autoencoder, encoder, decoder

from keras.datasets import mnist
import numpy as np

def load_datas():
  (x_train, _), (x_test, _) = mnist.load_data()

  x_train = x_train.astype('float32') / 255.
  x_test  = x_test .astype('float32') / 255.

  x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
  x_test  = x_test .reshape((len(x_test ), np.prod(x_test .shape[1:])))

  # print x_train.shape
  # print x_test.shape

  return x_train, x_test

# use Matplotlib (don't ask)
import matplotlib.pyplot as plt

def plot_history(network_history, title='Loss and accuracy (Keras model)'):
  plt.figure(figsize=(15,10))

  plt.subplot(211)
  plt.title(title)
  # plt.xlabel('Epochs')
  plt.ylabel('Loss')
  plt.plot(network_history.history['loss'])
  plt.plot(network_history.history['val_loss'])
  plt.legend(['Training', 'Validation'])

  plt.subplot(212)
  plt.xlabel('Epochs')
  plt.ylabel('Accuracy')
  plt.plot(network_history.history['acc'])
  plt.plot(network_history.history['val_acc'])
  plt.legend(['Training', 'Validation'], loc='lower right')

  plt.show()

autoencoder, encoder, decoder = create_autoencoder(784, 32)
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy', metrics=['accuracy'])

x_train, x_test = load_datas()

autoencoder_history = autoencoder.fit(x_train, x_train,
                epochs=100,
                batch_size=256,
                shuffle=True,
                validation_data=(x_test, x_test))
plot_history(autoencoder_history)

# encode and decode some digits
# note that we take them from the *test* set
encoded_imgs = encoder.predict(x_test)
decoded_imgs = decoder.predict(encoded_imgs)

n = 10  # how many digits we will display
plt.figure(figsize=(20, 4))
for i in range(n):
    # display original
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(x_test[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # display reconstruction
    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(decoded_imgs[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()
