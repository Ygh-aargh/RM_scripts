#!/usr/bin/python

import sys
import statsmodels.api as sm
import numpy as np
import math

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
np.linalg.lstsq(x,y)

print "influence on own troop on attack:", np.linalg.lstsq(x,y)[0][0][0]
print "influence of opponent's troop on attack:", np.linalg.lstsq(x,y)[0][1][0]
print "general's base attack:", np.linalg.lstsq(x,y)[0][2][0]

excl=[]
for i in range(0, len(data)):
    if (math.isnan(data[i, 4]) or # nonexistent
        data[i, 4] == data[i,8] or  # kill
        data[i, 4] == 0 or  # tactic
        data[i, 4] == data[i, 3]): # ADA or tactic
        excl.append(i)

x=np.transpose(np.vstack((np.delete(data[:, 8], excl), np.delete(data[:, 17], excl), np.ones(len(data)-len(excl)))))
y=np.vstack(np.delete(data[:, 4], excl))
np.linalg.lstsq(x,y)

print "\ninfluence on our troop on opponent's attack:", np.linalg.lstsq(x,y)[0][0][0]
print "influence of opponent's troop on attack:", np.linalg.lstsq(x,y)[0][1][0]
print "opponent's base attack:", np.linalg.lstsq(x,y)[0][2][0]

