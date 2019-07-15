import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.datasets import make_blobs
from random import randint
import json

class jsondat(object):
    def __init__(self, data):
        self.__dict__ = json.loads(data)

data=""
with open('out.json', 'r') as f:
    data = f.read()
Xy = jsondat(data)
epic = randint(1,1000)
# we create 40 separable points
X=[[0],[0]]
y = [1,0]
print(epic)
# fit the model, don't regularize for illustration purposes
clf = svm.SVC(kernel='rbf', gamma=1)
clf.fit(X, y)

plt.scatter(X[:][0], y[:][1], c=y, s=30, cmap=plt.cm.Paired)

# plot the decision function
ax = plt.gca()
xlim = ax.get_xlim()
ylim = ax.get_ylim()

# create grid to evaluate model
xx = np.linspace(xlim[0], xlim[1], 30)
yy = np.linspace(ylim[0], ylim[1], 30)
YY, XX = np.meshgrid(yy, xx)
xy = np.vstack([XX.ravel(), YY.ravel()]).T
Z = clf.decision_function(xy).reshape(XX.shape)

# plot decision boundary and margins
ax.contour(XX, YY, Z, colors='k', levels=[-1, 0, 1], alpha=0.5,
           linestyles=['--', '-', '--'])
# plot support vectors
ax.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=100,
           linewidth=1, facecolors='none', edgecolors='k')
plt.show()
