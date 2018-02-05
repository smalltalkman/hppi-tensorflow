from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, hppi

import tensorflow as tf
tf.logging.set_verbosity(tf.logging.INFO)

def main():
  # Load datasets.
  hppids = hppi.read_data_sets(os.getcwd()+"/data/09-hppids", one_hot=False)

  # Specify that all features have real-value data
  feature_columns = [tf.feature_column.numeric_column("x", shape=[1106])]

  # Build 3 layer DNN with 10, 20, 10 units respectively.
  classifier = tf.estimator.DNNClassifier(feature_columns=feature_columns,
                                          # input_layer_partitioner=None,
                                          hidden_units=[10, 20, 10],
                                          # activation_fn=tf.nn.relu,
                                          n_classes=2,
                                          # optimizer='Adagrad',
                                          model_dir="/tmp/hppi_model")
  # Define the training inputs
  train_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": hppids.train.datas},
      y=hppids.train.labels,
      num_epochs=None,
      shuffle=True,
      queue_capacity=60000)

  # Train model.
  classifier.train(input_fn=train_input_fn, steps=10000)

  # Define the test inputs
  test_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": hppids.test.datas},
      y=hppids.test.labels,
      num_epochs=1,
      shuffle=False)

  # Evaluate accuracy.
  accuracy_score = classifier.evaluate(input_fn=test_input_fn)["accuracy"]

  print("\nTest Accuracy: {0:f}\n".format(accuracy_score))

if __name__ == "__main__":
    main()
