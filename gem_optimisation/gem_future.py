#!/usr/bin/python

#import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.patches as patches
import gemprop

def find_possibilities(g1, g2, fg):

    # find all available gem combinations within the price range
    list = []
    for gg1 in gemprop.gemprop:
        if (gg1[2] >= g1[2] and gg1[2] <= g1[2] + fg):
            for gg2 in gemprop.gemprop:
                if (gg2[2] >= g2[2] and gg1[2] + gg2[2] <= g1[2] + g2[2] + fg):
                    list.append([gg1[0], gg2[0], gg1[1]+gg2[1], gg1[2]+gg2[2]])
    # print list

    # select best gem combinations for given strength
    lg = {}
    for gg in list:
        if (gg[2] in lg):
            if (lg[gg[2]][2] > gg[3]):
                lg[gg[2]] = [gg[0], gg[1], gg[3]]
        else:
            lg[gg[2]] = [gg[0], gg[1], gg[3]]

    # remove some expensive local peaks
    cost = 2 * gemprop.gemprop[len(gemprop.gemprop)-1][2]
    for tl in sorted(lg, reverse=True):
        if (lg[tl][2] > cost):
            # print "!",tl, lg[tl]
            del lg[tl]
        else:
            # print tl, lg[tl]
            cost = lg[tl][2]

    best = []
    for tl in sorted(lg):
        best.append([lg[tl][0], lg[tl][1], tl-g1[1]-g2[1], lg[tl][2]-g1[2]-g2[2]])
    # print best

    return best


import sys

if (len(sys.argv) != 8):
    print "Usage: ",sys.argv[0]," AL AR DL DR TL TR g"
    exit(-1)

tot_cost = 0
gi = []
for g in range(6):
    gi.append([])
    gn = sys.argv[1+g]
    if (gn[0] != "L"):
        gn = "L" + gn
    for gg in gemprop.gemprop:
        if (gn == gg[0]):
            gi[g] = gg
            break
    if (len(gi[g]) ==0):
        print "Can't interpret `", gn, "'"
        exit(-2)
    tot_cost += gi[g][2]

free_gems = int(sys.argv[7])

print("# Total cost: %d (%.1fk)" % (tot_cost, tot_cost/1024.))
print("# Attack : %d" % (5*(gi[0][1] + gi[1][1])))
print("# Defense: %d" % (3*(gi[2][1] + gi[3][1])))
print("# Troops : %d" % (8*(gi[4][1] + gi[5][1])))

# upgrade lists for attack, defense and troops
a_list = find_possibilities(gi[0], gi[1], free_gems)
d_list = find_possibilities(gi[2], gi[3], free_gems)
t_list = find_possibilities(gi[4], gi[5], free_gems)

print "\n# gem_cost stat+increase left_gem right_gem\n# Attack upgrades"
for i in a_list:
    print "%6d %4d %4s %4s" % (i[3], 5*i[2], i[0], i[1])

print "\n# Defense upgrades"
for i in d_list:
    print "%6d %4d %4s %4s" % (i[3], 3*i[2], i[0], i[1])

print "\n# Troops upgrades"
for i in t_list:
    print "%6d %4d %4s %4s" % (i[3], 8*i[2], i[0], i[1])
