#!/usr/bin/python

import math
import sys
import numpy as np

def length2steps(length, dice):
    ptable = np.zeros(length+dice.size)
    ptable[:dice.size]=dice
    stepdistr=[0]
    while ptable[:length].sum() > 0.:
        stepdistr.append(ptable[length:].sum())
        ptable[length:]=0.
        tmp=np.zeros(ptable.size+dice.size)
        for i in range(1,dice.size):
            tmp[i:i+ptable.size] += dice[i] * ptable
        ptable=tmp[:ptable.size]
    stepdistr.append(ptable[length:].sum())
    return stepdistr

steplist=[]
for line in sys.stdin:
    for s in line.split():
        steplist.append(int(s))

k6=np.ones(7)/6.
k6[0]=0.

for steps in steplist:
    stepdistr=length2steps(steps, k6)
    print steps, ":", stepdistr
