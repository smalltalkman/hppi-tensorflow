from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, hppi
from sklearn import svm
from sklearn.metrics import confusion_matrix

def main():
  # Load datasets.
  cwd = os.getcwd()
  data_sets_dir = cwd + "/data/09-hppids"
  hppids = hppi.read_data_sets(data_sets_dir, one_hot=False)
  train_datas, train_labels, test_datas, test_labels = hppids.shuffle().split()

  # train_datas  = train_datas [:100]
  # train_labels = train_labels[:100]
  # test_datas   = test_datas  [:100]
  # test_labels  = test_labels [:100]

  # train
  classifier = svm.SVC(kernel='linear', C=0.01)
  classifier.fit(train_datas, train_labels)

  # test
  mean_accuracy = classifier.score(test_datas, test_labels)
  print("mean_accuracy=", mean_accuracy)

  # predict
  # prediction_SVM = classifier.predict(test_datas)
  # confusion_matrix(test_labels, prediction_SVM)

if __name__ == "__main__":
    main()
