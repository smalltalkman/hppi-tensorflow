
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

def print_dividing_line(prompt=''):
  print('\n', '-'*80, '\n', '-'*3, prompt)

import warnings
warnings.filterwarnings("ignore")

import sklearn
sklearn.show_versions()

from sklearn.datasets import make_moons
X, y = make_moons(n_samples=500, noise=0.30, random_state=42)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# -------------------------------------------------------------------------------- #
print_dividing_line('VotingClassifier')

from sklearn.linear_model import LogisticRegression
log_clf = LogisticRegression()
from sklearn.svm import SVC
svc_clf = SVC()
from sklearn.ensemble import RandomForestClassifier
rf_clf = RandomForestClassifier()

from sklearn.ensemble import VotingClassifier
voting_clf = VotingClassifier( estimators=[("log", log_clf), ("svc", svc_clf), ("rf", rf_clf)], voting="hard" ) # soft

from sklearn.metrics import accuracy_score
for clf in ( log_clf, svc_clf, rf_clf, voting_clf ):
  clf.fit( X_train, y_train )
  y_pred = clf.predict( X_test )
  print( clf.__class__.__name__, accuracy_score(y_test, y_pred) )

# -------------------------------------------------------------------------------- #
print_dividing_line('BaggingClassifier')

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier
bag_clf = BaggingClassifier( DecisionTreeClassifier(), n_estimators=500, max_samples=100, bootstrap=True, n_jobs=-1 )

from sklearn.metrics import accuracy_score
bag_clf.fit( X_train, y_train )
y_pred = bag_clf.predict( X_test )
pred_score = accuracy_score( y_pred, y_test )
print( pred_score )

# -------------------------------------------------------------------------------- #
print_dividing_line('RandomForestClassifier & ExtraTreesClassifier')

from sklearn.ensemble import RandomForestClassifier
rf_clf = RandomForestClassifier( n_estimators=500, max_leaf_nodes=16, n_jobs=-1 )

from sklearn.ensemble import ExtraTreesClassifier
extra_tree_clf = ExtraTreesClassifier(n_estimators=500, max_leaf_nodes=16, n_jobs=-1)

from sklearn.metrics import accuracy_score
for clf in ( rf_clf, extra_tree_clf ):
  clf.fit( X_train, y_train )
  y_pred = clf.predict( X_test )
  print( clf.__class__.__name__, accuracy_score(y_test, y_pred) )

# -------------------------------------------------------------------------------- #
print_dividing_line('AdaBoostClassifier')

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
ada_clf = AdaBoostClassifier(
    DecisionTreeClassifier(max_depth=1), n_estimators=200,
    algorithm="SAMME.R", learning_rate=0.5, random_state=42)

from sklearn.metrics import accuracy_score
ada_clf.fit( X_train, y_train )
y_pred = ada_clf.predict( X_test )
pred_score = accuracy_score( y_pred, y_test )
print( pred_score )

# -------------------------------------------------------------------------------- #
print_dividing_line('GradientBoostingClassifier')

from sklearn.ensemble import GradientBoostingClassifier
gb_clf = AdaBoostClassifier()

from sklearn.metrics import accuracy_score
gb_clf.fit( X_train, y_train )
y_pred = gb_clf.predict( X_test )
pred_score = accuracy_score( y_pred, y_test )
print( pred_score )

# -------------------------------------------------------------------------------- #
print_dividing_line('HistGradientBoostingClassifier')

from sklearn.ensemble import HistGradientBoostingClassifier
hgb_clf = HistGradientBoostingClassifier()

from sklearn.metrics import accuracy_score
hgb_clf.fit( X_train, y_train )
y_pred = hgb_clf.predict( X_test )
pred_score = accuracy_score( y_pred, y_test )
print( pred_score )
