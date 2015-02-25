#!/usr/bin/python

import sys
import statsmodels.api as sm
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

#print sys.argv
#print len(sys.argv)

if (len(sys.argv) < 2):
    print "Usage: ",sys.argv[0]," .tsv_file"
    exit(-1)

#data=np.loadtxt(sys.argv[1])
data=np.genfromtxt(sys.argv[1], delimiter='\t')
#print data

excl=[]
for i in range(0, len(data)):
    if (math.isnan(data[i, 13]) or # nonexistent
        data[i, 13] == data[i,17] or  # kill
        data[i, 13] == 0 or  # tactic
        data[i, 13] == data[i, 12]): # ADA or tactic
        excl.append(i)

#print excl

x=np.transpose(np.vstack((np.delete(data[:, 8], excl), np.delete(data[:, 17], excl), np.ones(len(data)-len(excl)))))
y=np.vstack(np.delete(data[:, 13], excl))
a=np.linalg.lstsq(x,y)

print "influence on own troop on attack: ", a[0][0][0]
print "influence of opponent's troop on attack: ", a[0][1][0]
print "general's base attack: ", a[0][2][0]
print "sum squares: ",a[1][0]," L2?: ",np.sqrt(a[1][0]/np.sum(y*y))
print "#samples: ",len(y)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x[:, 0], x[:, 1], y)
ax.set_xlabel('Nadric')
ax.set_ylabel('enemy')
ax.set_zlabel('damage by Nadric')
X = np.arange(np.min(x[:, 0]), np.max(x[:, 0]), (np.max(x[:, 0]) - np.min(x[:, 0]))/ 8.)
Y = np.arange(np.min(x[:, 1]), np.max(x[:, 1]), (np.max(x[:, 1]) - np.min(x[:, 1]))/ 8.)
X, Y = np.meshgrid(X, Y)
Z = a[0][2][0] + a[0][0][0]*X + a[0][1][0]*Y
surf = ax.plot_wireframe(X, Y, Z)
plt.show()

excl=[]
for i in range(0, len(data)):
    if (math.isnan(data[i, 4]) or # nonexistent
        data[i, 4] == data[i,8] or  # kill
        data[i, 4] == 0 or  # tactic
#        data[i, 4] > 60 or
        data[i, 4] == data[i, 3]): # ADA or tactic
        excl.append(i)

x=np.transpose(np.vstack((np.delete(data[:, 8], excl), np.delete(data[:, 17], excl), np.ones(len(data)-len(excl)))))
y=np.vstack(np.delete(data[:, 4], excl))
a=np.linalg.lstsq(x,y)

print "\ninfluence on our troop on opponent's attack:", a[0][0][0]
print "influence of opponent's troop on attack:", a[0][1][0]
print "opponent's base attack:", a[0][2][0]
print "sum squares: ",a[1][0]," L2?: ",np.sqrt(a[1][0]/np.sum(y*y))
print "#samples: ",len(y)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x[:, 0], x[:, 1], y)
ax.set_xlabel('Nadric')
ax.set_ylabel('enemy')
ax.set_zlabel('damage by enemy')
X = np.arange(np.min(x[:, 0]), np.max(x[:, 0]), (np.max(x[:, 0]) - np.min(x[:, 0]))/ 8.)
Y = np.arange(np.min(x[:, 1]), np.max(x[:, 1]), (np.max(x[:, 1]) - np.min(x[:, 1]))/ 8.)
X, Y = np.meshgrid(X, Y)
Z = a[0][2][0] + a[0][0][0]*X + a[0][1][0]*Y
surf = ax.plot_wireframe(X, Y, Z)
plt.show()
