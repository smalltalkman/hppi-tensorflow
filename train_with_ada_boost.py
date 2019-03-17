from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, pandas, hppi
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import confusion_matrix, roc_curve, auc, average_precision_score, recall_score, log_loss

def train_and_test(data_sets_dir):
  # Load datasets.
  hppids = hppi.read_data_sets(data_sets_dir, one_hot=False)
  train_datas, train_labels, test_datas, test_labels = hppids.shuffle().split()

  # train_datas  = train_datas [:100]
  # train_labels = train_labels[:100]
  # test_datas   = test_datas  [:100]
  # test_labels  = test_labels [:100]

  # train
  classifier = AdaBoostClassifier(learning_rate=0.1)
  classifier.fit(train_datas, train_labels)

  # test
  mean_accuracy = classifier.score(test_datas, test_labels)
  # print("mean_accuracy=", mean_accuracy)

  # predict
  prediction = classifier.predict(test_datas)
  # confusion_matrix(test_labels, prediction)

  fpr, tpr, thresholds = roc_curve(test_labels, prediction)

  return (mean_accuracy,
          auc(fpr, tpr),
          average_precision_score(test_labels, prediction),
          recall_score(test_labels, prediction),
          log_loss(test_labels, prediction),
          )

def do_with(sub_dir):
  cwd = os.getcwd()
  df = pandas.DataFrame(columns=('accuracy', 'auc', 'average_precision', 'recall', 'log_loss', ))
  df.loc[len(df)] = train_and_test(cwd + "/data/" + sub_dir)
  df.to_csv(cwd + '/results/ada_boost-' + sub_dir + '.csv')

def main():
  do_with("02-ct-bin")
  do_with("03-ac-bin")
  do_with("04-ld-bin")
  do_with("05-mos-bin")
  do_with("09-hppids")

if __name__ == "__main__":
    main()
