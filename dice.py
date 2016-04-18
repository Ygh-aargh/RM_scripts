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

def convolve_two(t1, t2):
    t = np.zeros(t1.size+t2.size-1)
    for i in range(t1.size):
        t[i:i+t2.size] += t1[i] * t2
    return t

steplist=[]
for line in sys.stdin:
    for s in line.split():
        steplist.append(int(s))

k6=np.ones(7)/6.
k6[0]=0.

dictable=dict()
for steps in set(steplist):
    stepdistr=length2steps(steps, k6)
    dictable[steps]=stepdistr

print "Probabilities for single routes of length n\n  n : one move, two moves, ..., n moves\n"
for i in sorted(dictable):
    pline = "%3d :" % (i)
    gline = (len(pline)*' ')
    p01 = False
    for p in dictable[i][1:]:
        pline += " %-9.3g" % (p)
        gline += " %-9s" % (int(10*p)*'+')
        if (p >= 0.1):
            p01 = True
    print pline
    if (p01):
        print gline
    print ""

t=np.ones(1)
for t1 in steplist:
    t=convolve_two(t, np.asarray(dictable[t1]))

print "\nMost probable number of moves for a set of routes with lengths ",steplist,"\nn moves, probability of n moves, probability of up to n moves\n%4s %7s%% %7s%%" % ('n','p(n)','p(m<=n)')

for i in range(t.size):
    if ((t[i]> 1e-3 and abs(t[:i+1].sum()-0.5) < 0.499) or t[i]>0.01):
        print "%4d %7.1f%% %7.1f%% %s" % (i, 100*t[i], 100*t[:i+1].sum(), int(50*t[i]/t[:].max())*'+')
