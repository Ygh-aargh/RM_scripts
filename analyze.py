#!/usr/bin/python

import sys
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy import stats
import csv

def plot3D(name):
    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.add_subplot(121, projection='3d')
    ax.scatter(x[:, 0], x[:, 1], y)
    ax.set_xlabel('Nadric')
    ax.set_ylabel('enemy')
    ax.set_zlabel('damage by ' + name)
    X = np.linspace(np.min(x[:, 0]), np.max(x[:, 0]), num=8)
    Y = np.linspace(np.min(x[:, 1]), np.max(x[:, 1]), num=8)
    X, Y = np.meshgrid(X, Y)
    Z = a[0][2][0] + a[0][0][0]*X + a[0][1][0]*Y
    ax.plot_wireframe(X, Y, Z)

    ax = fig.add_subplot(122, projection='3d')
    ax.scatter(x[:, 0], x[:, 1], y[:, 0] - (a[0][2][0] + a[0][0][0]*x[:, 0] + a[0][1][0]*x[:, 1]))
    ax.set_xlabel('Nadric')
    ax.set_ylabel('enemy')
    ax.set_zlabel('residual(damage)')

    plt.show()

def find_excl(column, limit=-1):
    excl=[]
    for i in range(0, len(data)):
        if (data[i, column] == data[i, column-2] or # kill
        ((limit > 0) and (data[i, column] > float(limit)))): # unreduced
            excl.append(i)
    return excl

def find_fit(column, limit=-1):
    excl=find_excl(column, limit)
    x=np.transpose(np.vstack((np.delete(data[:, 0], excl), np.delete(data[:, 1], excl), np.ones(len(data)-len(excl)))))
    y=np.vstack(np.delete(data[:, column], excl))
    return np.linalg.lstsq(x,y),x,y

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def load_data(fname):
    data=[]
    with open(fname) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        for line in tsvreader:
            if (is_number(line[8]) and is_number(line[17]) and # we have valid troop counts):
                len(line[0]) + len(line[9]) + len(line[18]) == 0): # no tactic, ADA or other comments
                data.append([line[8], line[17], line[4], line[13]])
    return data

#print sys.argv
#print len(sys.argv)

if (len(sys.argv) < 2):
    print "Usage: ",sys.argv[0]," .tsv_file"
    exit(-1)

data=np.array(load_data(sys.argv[1]), dtype=float)
#data=np.loadtxt(sys.argv[1])
#data=np.genfromtxt(sys.argv[1], delimiter='\t')
#print data

a,x,y=find_fit(3)
print "influence on own troop on attack: ", a[0][0][0]
print "influence of opponent's troop on attack: ", a[0][1][0]
print "general's base attack: ", a[0][2][0]
if (len(a[1]) >0):
    print "sum squares: ",a[1][0]," L2?: ",np.sqrt(a[1][0]/np.sum(y*y))
print "Residues: #samples, (min, max), average, variance, skew, kurtosis", stats.describe(y[:, 0] - (a[0][2][0] + a[0][0][0]*x[:, 0] + a[0][1][0]*x[:, 1]))
plot3D("Nadric")

if (len(sys.argv) >= 3):
    a,x,y=find_fit(2, limit=sys.argv[2])
else:
    a,x,y=find_fit(2)

print "\ninfluence on our troop on opponent's attack:", a[0][0][0]
print "influence of opponent's troop on attack:", a[0][1][0]
print "opponent's base attack:", a[0][2][0]
if (len(a[1]) >0):
    print "sum squares: ",a[1][0]," L2?: ",np.sqrt(a[1][0]/np.sum(y*y))
print "Residues: #samples, (min, max), average, variance, skew, kurtosis", stats.describe(y[:, 0] - (a[0][2][0] + a[0][0][0]*x[:, 0] + a[0][1][0]*x[:, 1]))
plot3D("enemy")
