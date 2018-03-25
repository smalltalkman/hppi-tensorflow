from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, hppi

import tensorflow as tf
tf.logging.set_verbosity(tf.logging.INFO)

def once(data_sets_dir, data_sets_info
       , num_input, hidden_units, activation_fn, num_classes, optimizer, learning_rate, dnn_info
       , num_steps
       , model_dir_root
       , result_dir_root
       ):
  model_info = "_{0}({1:d}x{2:d})_{3}_{4}_{5:g}".format(
                 data_sets_info
               , num_input
               , num_classes
               , 'x'.join([str(n) for n in hidden_units])
               , dnn_info
               , learning_rate
               )
  model_dir = model_dir_root+model_info
  result_file = result_dir_root+model_info+".txt"

  # Load datasets.
  hppids = hppi.read_data_sets(data_sets_dir, one_hot=False)

  # Specify that all features have real-value data
  feature_columns = [tf.feature_column.numeric_column("x", shape=[num_input])]

  # Build 3 layer DNN with 10, 20, 10 units respectively.
  classifier = tf.estimator.DNNClassifier(feature_columns=feature_columns,
                                          # input_layer_partitioner=None,
                                          # hidden_units=[10, 20, 10],
                                          hidden_units=hidden_units,
                                          # activation_fn=tf.nn.relu,
                                          activation_fn=activation_fn,
                                          n_classes=num_classes,
                                          # optimizer='Adagrad',
                                          optimizer=optimizer(learning_rate=learning_rate),
                                          model_dir=model_dir)
  # Define the training inputs
  train_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": hppids.train.datas},
      y=hppids.train.labels,
      num_epochs=None,
      shuffle=True,
      queue_capacity=hppids.train.length)

  # Train model.
  classifier.train(input_fn=train_input_fn, steps=num_steps)

  # Define the test inputs
  test_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": hppids.test.datas},
      y=hppids.test.labels,
      num_epochs=1,
      shuffle=False)

  # Evaluate accuracy.
  #accuracy_score = classifier.evaluate(input_fn=test_input_fn)["accuracy"]
  # Evaluate scores.
  scores = classifier.evaluate(input_fn=test_input_fn)
  scores_str =   "global_step = {0:08d}".format(scores["global_step"]) \
             + ", accuracy = {0:8g}".format(scores["accuracy"]) \
             + ", accuracy_baseline = {0:8g}".format(scores["accuracy_baseline"]) \
             + ", auc = {0:8g}".format(scores["auc"]) \
             + ", auc_precision_recall = {0:8g}".format(scores["auc_precision_recall"]) \
             + ", average_loss = {0:8g}".format(scores["average_loss"]) \
             + ", label/mean = {0:8g}".format(scores["label/mean"]) \
             + ", loss = {0:8g}".format(scores["loss"]) \
             + ", prediction/mean = {0:8g}".format(scores["prediction/mean"]) \

  #print("\nTest Accuracy: {0:f}\n".format(accuracy_score))
  print("\nTest scores: {0}\n".format(scores_str))

  with open(result_file, "a") as file:
    file.write(scores_str+"\n")

def more(times
        , data_sets_dir, data_sets_info
        , num_input, hidden_units, activation_fn, num_classes, optimizer, learning_rate, dnn_info
        , num_steps
        , model_dir_root
        , result_dir_root
        ):
    for _ in range(times):
        once( data_sets_dir, data_sets_info
            , num_input, hidden_units, activation_fn, num_classes, optimizer, learning_rate, dnn_info
            , num_steps
            , model_dir_root
            , result_dir_root
            )

def main():
    times = 1
    cwd = os.getcwd()
    bin_dir_root = cwd+"/data/predict_PPI"
    dirs = ["C.elegan", "Drosophila", "E.coli", "Human", "Yeast"]
    hidden_units = [256,256,256]
    activation_fn = tf.nn.relu
    optimizer = tf.train.AdamOptimizer
    learning_rate = 0.01 # 0.01 => 0.001 => 0.0001
    dnn_info = "relu_adam"
    num_steps = 10000
    model_dir_root = cwd+"/model/train_with_tf_estimator"
    result_dir_root = cwd+"/model/result_of_tf_estimator"
    for dir in dirs:
        bin_dir = bin_dir_root + "/" + dir + "/bin"
        more(times, bin_dir+"/ct",    "predict_PPI_{}_ct".format(dir),     686, hidden_units, activation_fn, 2, optimizer, learning_rate, dnn_info, num_steps, model_dir_root, result_dir_root)
        more(times, bin_dir+"/ac",    "predict_PPI_{}_ac".format(dir),     420, hidden_units, activation_fn, 2, optimizer, learning_rate, dnn_info, num_steps, model_dir_root, result_dir_root)
        more(times, bin_dir+"/ct+ac", "predict_PPI_{}_ct+ac".format(dir), 1106, hidden_units, activation_fn, 2, optimizer, learning_rate, dnn_info, num_steps, model_dir_root, result_dir_root)

if __name__ == "__main__":
    main()
