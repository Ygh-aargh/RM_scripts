#!/usr/bin/python

import sys
import statsmodels.api as sm
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def plot3D(name):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x[:, 0], x[:, 1], y)
    ax.set_xlabel('Nadric')
    ax.set_ylabel('enemy')
    ax.set_zlabel('damage by ' + name)
    X = np.linspace(np.min(x[:, 0]), np.max(x[:, 0]), num=8)
    Y = np.linspace(np.min(x[:, 1]), np.max(x[:, 1]), num=8)
    X, Y = np.meshgrid(X, Y)
    Z = a[0][2][0] + a[0][0][0]*X + a[0][1][0]*Y
    surf = ax.plot_wireframe(X, Y, Z)
    plt.show()

def find_excl(column, limit=-1):
    excl=[]
    for i in range(0, len(data)):
        if (math.isnan(data[i, column]) or # nonexistent
        data[i, column] == data[i, column+4] or # kill
        data[i, column] == 0 or # tactic
        ((limit > 0) and (data[i, column] > float(limit))) or # unreduced
        data[i, column] == data[i, column-1]): # ADA or tactic
            excl.append(i)
    return excl

def find_fit(column, limit=-1):
    excl=find_excl(column, limit)
    x=np.transpose(np.vstack((np.delete(data[:, 8], excl), np.delete(data[:, 17], excl), np.ones(len(data)-len(excl)))))
    y=np.vstack(np.delete(data[:, column], excl))
    return np.linalg.lstsq(x,y),x,y

#print sys.argv
#print len(sys.argv)

if (len(sys.argv) < 2):
    print "Usage: ",sys.argv[0]," .tsv_file"
    exit(-1)

#data=np.loadtxt(sys.argv[1])
data=np.genfromtxt(sys.argv[1], delimiter='\t')
#print data

a,x,y=find_fit(13)
print "influence on own troop on attack: ", a[0][0][0]
print "influence of opponent's troop on attack: ", a[0][1][0]
print "general's base attack: ", a[0][2][0]
print "sum squares: ",a[1][0]," L2?: ",np.sqrt(a[1][0]/np.sum(y*y))
print "#samples: ",len(y)
plot3D("Nadric")

if (len(sys.argv) >= 3):
    a,x,y=find_fit(4, limit=sys.argv[2])
else:
    a,x,y=find_fit(4)

print "\ninfluence on our troop on opponent's attack:", a[0][0][0]
print "influence of opponent's troop on attack:", a[0][1][0]
print "opponent's base attack:", a[0][2][0]
print "sum squares: ",a[1][0]," L2?: ",np.sqrt(a[1][0]/np.sum(y*y))
print "#samples: ",len(y)
plot3D("enemy")
