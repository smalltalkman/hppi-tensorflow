from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from datetime import datetime

import os, hppi

import tensorflow as tf
tf.logging.set_verbosity(tf.logging.INFO)

def main():
  # Load datasets.
  hppids = hppi.read_data_sets(data_sets_dir, one_hot=False)

  # Specify that all features have real-value data
  feature_columns = [tf.feature_column.numeric_column("x", shape=[num_input])]

  # Build 3 layer DNN with 10, 20, 10 units respectively.
  classifier = tf.estimator.DNNClassifier(feature_columns=feature_columns,
                                          # input_layer_partitioner=None,
                                          # hidden_units=[10, 20, 10],
                                          # hidden_units=[256, 256, 256],
                                          hidden_units=hidden_units,
                                          # activation_fn=tf.nn.relu,
                                          n_classes=num_classes,
                                          # optimizer='Adagrad',
                                          # optimizer=tf.train.AdamOptimizer(learning_rate=learning_rate),
                                          optimizer=optimizer,
                                          dropout=dropout,
                                          model_dir=model_dir)
  # Define the training inputs
  train_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": hppids.train.datas},
      y=hppids.train.labels,
      batch_size=batch_size,
      num_epochs=None,
      shuffle=True,
      queue_capacity=hppids.train.length)

  # Train model.
  begin_time = datetime.now()
  classifier.train(input_fn=train_input_fn, steps=num_steps)
  end_time = datetime.now()
  train_time = (end_time-begin_time).total_seconds()/num_steps*100

  # Define the test inputs
  test_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": hppids.test.datas},
      y=hppids.test.labels,
      batch_size=batch_size,
      num_epochs=1,
      shuffle=False)

  # Evaluate accuracy.
  #accuracy_score = classifier.evaluate(input_fn=test_input_fn)["accuracy"]
  # Evaluate scores.
  begin_time = datetime.now()
  scores = classifier.evaluate(input_fn=test_input_fn)
  end_time = datetime.now()
  test_time = (end_time-begin_time).total_seconds()

  scores_str =   "global_step = {0:08d}".format(scores["global_step"]) \
             + ", accuracy = {0:8g}".format(scores["accuracy"]) \
             + ", accuracy_baseline = {0:8g}".format(scores["accuracy_baseline"]) \
             + ", auc = {0:8g}".format(scores["auc"]) \
             + ", auc_precision_recall = {0:8g}".format(scores["auc_precision_recall"]) \
             + ", average_loss = {0:8g}".format(scores["average_loss"]) \
             + ", label/mean = {0:8g}".format(scores["label/mean"]) \
             + ", loss = {0:8g}".format(scores["loss"]) \
             + ", prediction/mean = {0:8g}".format(scores["prediction/mean"]) \
             + ", train_time = {0:8g}".format(train_time) \
             + ", test_time = {0:8g}".format(test_time) \

  #print("\nTest Accuracy: {0:f}\n".format(accuracy_score))
  print("\nTest scores: {0}\n".format(scores_str))

  with open(result_file, "a") as file:
    file.write(scores_str+"\n")

if __name__ == "__main__":

  from sys import argv
  _, target = argv

  import json
  with open('train_with_tf_estimator_hppi.json') as config_file:
    configs = json.load(config_file)

  model = configs['models'][target]
  data_set = configs['data_sets'][model['data_sets_info']]
  coding = configs['coding'][data_set['coding']]

  # Training Parameters
  learning_rate = model['learning_rate'] # 0.001 # 0.01 => 0.001 => 0.0001
  dropout = model['dropout'] # 0.1
  # batch_size = 128
  if 'batch' in model:
    batch_size = model['batch']
  else:
    batch_size = 128
  num_steps = 10000
  times = model['times'] # 1

  # Network Parameters
  num_input = coding['num_input'] # 686 # HPPI data input
  num_classes = coding['num_classes'] # 2 # HPPI total classes
  hidden_units = model['hidden_units'] # [256, 256, 256]
  activation_fn = tf.nn.relu
  # optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
  if 'optimizer' in model:
    optimizer_name = model['optimizer']
    from tensorflow_estimator.python.estimator.canned import optimizers
    optimizer = optimizers.get_optimizer_instance(optimizer_name, learning_rate=learning_rate)
  else:
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)

  cwd = os.getcwd()
  data_sets_dir = cwd+"/"+data_set['dir'] # "/data/02-ct-bin"
  # model_info = "_{0}({1:d}x{2:d})_{3}_{4}_{5}_{6:g}_dropout_{7:g}".format(model['data_sets_info'], num_input, num_classes, 'x'.join([str(n) for n in hidden_units]), activation_fn.__name__, optimizer.get_name(), learning_rate, dropout)
  model_info = "_{0}".format(target)
  model_dir = cwd+"/model/train_with_tf_estimator"+model_info
  result_file = cwd+"/model/result_of_tf_estimator"+model_info+".txt"

  for _ in range(times):
    main()
