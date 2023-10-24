# -*- coding: utf-8 -*-
"""isit_5-6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GrqYAP7cME80K2rmjAulV2-2JD7GxTFg

#Unpacking and encoding dataframe#
"""

import pandas as pd

# Reading data from csv
df = pd.read_csv("ecoli.data", sep="\s+", names=["Sequence name",  "mcg", "gvh", "lip", "chg", "aac", "alm1",
                                       "alm2", "class"])

df

pip install umap-learn

pip install umap

from itertools import count
import seaborn as sns
import umap.umap_ as umap
import numpy as np
from sklearn.manifold import TSNE
from sklearn.preprocessing import LabelEncoder

df_one_hot = pd.get_dummies(df, columns=["Sequence name"])

le = LabelEncoder()
df_one_hot["class"] = le.fit_transform(df["class"])

df_one_hot

"""#Functions section#

T-SNE function
"""

def t_sne_draw(encoded_dataframe, n_components, perplexity, angle):
  X_embedded = TSNE(n_components=n_components, perplexity=perplexity, angle=angle).fit_transform(encoded_dataframe)
  X, Y = X_embedded[:, 0], X_embedded[:, 1]
  sns.scatterplot(x=X, y=Y, hue=encoded_dataframe["class"], palette="deep")

"""UMAP function"""

def umap_draw(encoded_dataframe, n_components, n_neighbors, min_dist):
  reducer = umap.UMAP(n_neighbors=n_neighbors, min_dist=min_dist, n_components=n_components, metric='euclidean')
  embedding = reducer.fit_transform(encoded_dataframe)
  X_umap, Y_umap = embedding[:, 0], embedding[:, 1]
  sns.scatterplot(x=X_umap, y=Y_umap, hue=encoded_dataframe["class"], palette="deep")

"""#SVM classifier with RBF kernel#"""

from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score, multilabel_confusion_matrix

# Splitting on test and train
X_train, X_test, y_train, y_test = train_test_split(df_one_hot.loc[:, df_one_hot.columns != "class"], df_one_hot["class"],
                                                    test_size=0.3, shuffle=True)

X_for_test = X_test
X_test_neigh = X_test
X_test_rf = X_test
y_test_neigh = y_test
y_test_rf = y_test

# Creating and training classifier with RBF kernel
clf = svm.SVC(C=5,kernel="rbf")
clf.fit(X_train, y_train)

# Printing support vectors
len(clf.support_vectors_)

# Predicting values
pred = clf.predict(X_test)

# Precision
clf.score(X_test, y_test, sample_weight=None)

# 'micro': Calculate metrics globally by counting the total true positives, false negatives and false positives.
print(f1_score(pred, y_test, average="micro"))
print(precision_score(pred, y_test, average="micro"))
print(recall_score(pred, y_test, average="micro"))

# Check on confusion matrix
multilabel_confusion_matrix(y_test, pred)

"""#SVM classifier with linear kernel#"""

# Creating and training classifier with linear kernel
clf = svm.SVC(C=5, kernel="linear")
clf.fit(X_train, y_train)

# Printing support vectors
len(clf.support_vectors_)

# Predicting values
pred = clf.predict(X_test)

# Precision
clf.score(X_test, y_test, sample_weight=None)

# 'micro': Calculate metrics globally by counting the total true positives, false negatives and false positives.
print(f1_score(pred, y_test, average="micro"))
print(precision_score(pred, y_test, average="micro"))
print(recall_score(pred, y_test, average="micro"))

"""#SVM classifier with polynomial kernel#"""

# Creating and training classifier with linear kernel
clf = svm.SVC(C=5, kernel="poly")
clf.fit(X_train, y_train)

# Printing support vectors
len(clf.support_vectors_)

# Predicting values
pred = clf.predict(X_test)

# Precision
clf.score(X_test, y_test, sample_weight=None)

# 'micro': Calculate metrics globally by counting the total true positives, false negatives and false positives.
print(f1_score(pred, y_test, average="micro"))
print(precision_score(pred, y_test, average="micro"))
print(recall_score(pred, y_test, average="micro"))

"""#SVM classifier with sigmoid kernel#"""

# Creating and training classifier with linear kernel
clf = svm.SVC(C=5, kernel="sigmoid")
clf.fit(X_train, y_train)

# Printing support vectors
len(clf.support_vectors_)

# Predicting values
pred = clf.predict(X_test)

# Precision
clf.score(X_test, y_test, sample_weight=None)

# 'micro': Calculate metrics globally by counting the total true positives, false negatives and false positives.
print(f1_score(pred, y_test, average="micro"))
print(precision_score(pred, y_test, average="micro"))
print(recall_score(pred, y_test, average="micro"))

"""#Grid search for SVM classifier#"""

from sklearn.model_selection import GridSearchCV

parameters = {"kernel":("linear", "rbf", "sigmoid", "poly"), "C":list(range(1, 11)), "class_weight": [None, "balanced"]}
scoring = ['accuracy','f1_macro', 'recall']
svc = svm.SVC()

clf = GridSearchCV(svc, parameters, n_jobs=4, verbose=3, refit=False, cv=2)

clf.fit(X_train, y_train)

sorted(clf.cv_results_.keys())

clf.best_params_

"""#Training using best parameters for SVM classifier according to Grid search and plotting using T-SNE and UMAP#"""

# Creating and training classifier with linear kernel
clf = svm.SVC(**clf.best_params_)
clf.fit(X_train, y_train)

# Printing support vectors
len(clf.support_vectors_)

# Predicting values
pred = clf.predict(X_test)

pred_test = pd.Series(pred, name="class")

# Precision
clf.score(X_test, y_test, sample_weight=None)

# 'micro': Calculate metrics globally by counting the total true positives, false negatives and false positives.
print(f1_score(pred, y_test, average="micro"))
print(precision_score(pred, y_test, average="micro"))
print(recall_score(pred, y_test, average="micro"))

X_test.reset_index(drop=True, inplace=True)
y_pred = pd.DataFrame(pred_test)
new_df = pd.concat([X_test, y_pred], axis=1)
# new_df.drop('index', axis=1, inplace=True)

new_df

y_for_test = pd.DataFrame(y_test)
y_for_test.reset_index(drop=True, inplace=True)
y_for_test

X_for_test

new_df_test = pd.concat([X_for_test, y_for_test], axis=1)
new_df_test

# T-SNE test plot
t_sne_draw(new_df_test, 2, 15, 0.6)

# UMAP test plot
umap_draw(new_df_test, 2, 15, 0.6)

# T-SNE prediction plot
t_sne_draw(new_df, 2, 15, 0.6)

# UMAP prediction plot
umap_draw(new_df, 2, 15, 0.6)

"""#KNN classifier with Minkowski metric and different algorithms#

Ball tree algorithm
"""

from sklearn.neighbors import KNeighborsClassifier

# Training model
neigh = KNeighborsClassifier(n_neighbors=20, algorithm="ball_tree", metric="minkowski")
neigh.fit(X_train, y_train)

# Predicting values
pred_neigh = neigh.predict(X_test_neigh)
# Precision
neigh.score(X_test_neigh, y_test_neigh, sample_weight=None)

# Accuracy
print(f1_score(pred_neigh, y_test_neigh, average="micro"))
print(precision_score(pred_neigh, y_test_neigh, average="micro"))
print(recall_score(pred_neigh, y_test_neigh, average="micro"))

"""KD tree algorithm"""

# Training model
neigh = KNeighborsClassifier(n_neighbors=20, algorithm="kd_tree", metric="minkowski")
neigh.fit(X_train, y_train)

# Predicting values
pred_neigh = neigh.predict(X_test_neigh)
# Precision
neigh.score(X_test_neigh, y_test_neigh, sample_weight=None)

# Accuracy
print(f1_score(pred_neigh, y_test_neigh, average="micro"))
print(precision_score(pred_neigh, y_test_neigh, average="micro"))
print(recall_score(pred_neigh, y_test_neigh, average="micro"))

"""Brute algorithm"""

neigh = KNeighborsClassifier(n_neighbors=20, algorithm="brute", metric="minkowski")
neigh.fit(X_train, y_train)

# Predicting values
pred_neigh = neigh.predict(X_test_neigh)
# Precision
neigh.score(X_test_neigh, y_test_neigh, sample_weight=None)

# Accuracy
print(f1_score(pred_neigh, y_test_neigh, average="micro"))
print(precision_score(pred_neigh, y_test_neigh, average="micro"))
print(recall_score(pred_neigh, y_test_neigh, average="micro"))

"""#KNN classifier with Manhattan metric and different algorithms#

Ball tree algorithm
"""

neigh = KNeighborsClassifier(n_neighbors=20, algorithm="ball_tree", metric="manhattan")
neigh.fit(X_train, y_train)

# Predicting values
pred_neigh = neigh.predict(X_test_neigh)
# Precision
neigh.score(X_test_neigh, y_test_neigh, sample_weight=None)

# Accuracy
print(f1_score(pred_neigh, y_test_neigh, average="micro"))
print(precision_score(pred_neigh, y_test_neigh, average="micro"))
print(recall_score(pred_neigh, y_test_neigh, average="micro"))

"""KD tree algorithm"""

neigh = KNeighborsClassifier(n_neighbors=20, algorithm="kd_tree", metric="manhattan")
neigh.fit(X_train, y_train)

# Predicting values
pred_neigh = neigh.predict(X_test_neigh)
# Precision
neigh.score(X_test_neigh, y_test_neigh, sample_weight=None)

# Accuracy
print(f1_score(pred_neigh, y_test_neigh, average="micro"))
print(precision_score(pred_neigh, y_test_neigh, average="micro"))
print(recall_score(pred_neigh, y_test_neigh, average="micro"))

"""Brute algorithm"""

neigh = KNeighborsClassifier(n_neighbors=20, algorithm="kd_tree", metric="manhattan")
neigh.fit(X_train, y_train)

# Predicting values
pred_neigh = neigh.predict(X_test_neigh)
# Precision
neigh.score(X_test_neigh, y_test_neigh, sample_weight=None)

# Accuracy
print(f1_score(pred_neigh, y_test_neigh, average="micro"))
print(precision_score(pred_neigh, y_test_neigh, average="micro"))
print(recall_score(pred_neigh, y_test_neigh, average="micro"))

"""#KNN classifier with Euclidean metric and different algorithms#

Ball tree algorithm
"""

neigh = KNeighborsClassifier(n_neighbors=20, algorithm="ball_tree", metric="euclidean")
neigh.fit(X_train, y_train)

# Predicting values
pred_neigh = neigh.predict(X_test_neigh)
# Precision
neigh.score(X_test_neigh, y_test_neigh, sample_weight=None)

# Accuracy
print(f1_score(pred_neigh, y_test_neigh, average="micro"))
print(precision_score(pred_neigh, y_test_neigh, average="micro"))
print(recall_score(pred_neigh, y_test_neigh, average="micro"))

"""KD tree algorithm"""

neigh = KNeighborsClassifier(n_neighbors=20, algorithm="kd_tree", metric="euclidean")
neigh.fit(X_train, y_train)

# Predicting values
pred_neigh = neigh.predict(X_test_neigh)
# Precision
neigh.score(X_test_neigh, y_test_neigh, sample_weight=None)

# Accuracy
print(f1_score(pred_neigh, y_test_neigh, average="micro"))
print(precision_score(pred_neigh, y_test_neigh, average="micro"))
print(recall_score(pred_neigh, y_test_neigh, average="micro"))

"""Brute algorithm"""

neigh = KNeighborsClassifier(n_neighbors=20, algorithm="brute", metric="euclidean")
neigh.fit(X_train, y_train)

# Predicting values
pred_neigh = neigh.predict(X_test_neigh)
# Precision
neigh.score(X_test_neigh, y_test_neigh, sample_weight=None)

# Accuracy
print(f1_score(pred_neigh, y_test_neigh, average="micro"))
print(precision_score(pred_neigh, y_test_neigh, average="micro"))
print(recall_score(pred_neigh, y_test_neigh, average="micro"))

"""#Grid search for KNN classifier#"""

parameters = {"n_neighbors":list(range(5, 30)), "algorithm":("brute", "kd_tree", "ball_tree"),
              "metric":["minkowski", "manhattan", "euclidean"]}

kneigh = KNeighborsClassifier()

neigh = GridSearchCV(kneigh, parameters, n_jobs=4, verbose=3, refit=False, cv=2)

neigh.fit(X_train, y_train)

sorted(neigh.cv_results_.keys())

neigh.best_params_

"""#Training using best parameters for KNN classifier according to Grid search  and plotting using T-SNE and UMAP#

"""

neigh = KNeighborsClassifier(**neigh.best_params_)
neigh.fit(X_train, y_train)

# Predicting values
pred_neigh = clf.predict(X_test_neigh)
# Precision
neigh.score(X_test_neigh, y_test_neigh, sample_weight=None)

print(f1_score(pred_neigh, y_test_neigh, average="micro"))
print(precision_score(pred_neigh, y_test_neigh, average="micro"))
print(recall_score(pred_neigh, y_test_neigh, average="micro"))

X_test_neigh.reset_index(drop=True, inplace=True)
y_pred = pd.DataFrame(pred_neigh)
y_pred.columns = ["class"]
new_df_neigh = pd.concat([X_test_neigh, y_pred], axis=1)

y_pred

new_df_neigh

# T-SNE prediction plot
t_sne_draw(new_df_neigh, 2, 15, 0.6)

# UMAP prediction plot
umap_draw(new_df_neigh, 2, 15, 0.6)

"""#RF classifier with Gini impurity criterion#"""

from sklearn.ensemble import RandomForestClassifier

rfc = RandomForestClassifier(n_estimators=200, criterion="gini")
rfc.fit(X_train, y_train)

# Predicting values
pred_rfc = rfc.predict(X_test_rf)
# Precision
rfc.score(X_test_rf, y_test_rf, sample_weight=None)

print(f1_score(pred_rfc, y_test_rf, average="micro"))
print(precision_score(pred_rfc, y_test_rf, average="micro"))
print(recall_score(pred_rfc, y_test_rf, average="micro"))

"""#RF classifier with Entropy criterion#"""

rfc = RandomForestClassifier(n_estimators=200, criterion="entropy")
rfc.fit(X_train, y_train)

# Predicting values
pred_rfc = rfc.predict(X_test_rf)
# Precision
rfc.score(X_test_rf, y_test_rf, sample_weight=None)

print(f1_score(pred_rfc, y_test_rf, average="micro"))
print(precision_score(pred_rfc, y_test_rf, average="micro"))
print(recall_score(pred_rfc, y_test_rf, average="micro"))

"""#RF classifier with Log loss criterion#"""

rfc = RandomForestClassifier(n_estimators=200, criterion="log_loss")
rfc.fit(X_train, y_train)

# Predicting values
pred_rfc = rfc.predict(X_test_rf)
# Precision
rfc.score(X_test_rf, y_test_rf, sample_weight=None)

print(f1_score(pred_rfc, y_test_rf, average="micro"))
print(precision_score(pred_rfc, y_test_rf, average="micro"))
print(recall_score(pred_rfc, y_test_rf, average="micro"))

"""#Grid search for RF classifier#"""

parameters = {"n_estimators":list(range(100, 200, 25)), "criterion":("gini", "entropy", "log_loss"), "max_depth":list(range(3, 6))}
rf = RandomForestClassifier()

rfc = GridSearchCV(rf, parameters, n_jobs=4, verbose=3, refit=False, cv=2)

rfc.fit(X_train, y_train)

sorted(rfc.cv_results_.keys())

rfc.best_params_

"""#Training using best parameters for RF classifier according to Grid search  and plotting using T-SNE and UMAP#"""

rfc = RandomForestClassifier(**rfc.best_params_)
rfc.fit(X_train, y_train)

# Predicting values
pred_rf = clf.predict(X_test_rf)
# Precision
neigh.score(X_test_rf, y_test_rf, sample_weight=None)

print(f1_score(pred_rf, y_test_rf, average="micro"))
print(precision_score(pred_rf, y_test_rf, average="micro"))
print(recall_score(pred_rf, y_test_rf, average="micro"))

X_test_rf.reset_index(drop=True, inplace=True)
y_pred = pd.DataFrame(pred_rf)
y_pred.columns = ["class"]
new_df_rf = pd.concat([X_test_rf, y_pred], axis=1)
# new_df.drop('index', axis=1, inplace=True)

new_df_rf

# T-SNE prediction plot
t_sne_draw(new_df_rf, 2, 15, 0.6)

# UMAP prediction plot
umap_draw(new_df_rf, 2, 15, 0.6)