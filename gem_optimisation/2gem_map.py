#!/usr/bin/python

gemprop=[["L0", 0, 0],
["L1", 1, 1],
["L2", 2, 2],
["L3", 3, 4],
["L4", 4, 8],
["L5", 6, 16],
["L6", 8, 32],
["L7", 11, 64],
["L8", 15, 128],
["L9", 21, 256],
["L10", 30, 512],
["L11", 45, 1024],
["L12", 60, 2048],
["L13", 80, 4096],
["L14", 100, 8192],
["L1*", 120, 16384],
["L2*", 125, 16884],
["L3*", 130, 17484],
["L4*", 135, 18284],
["L5*", 140, 19284],
["L6*", 145, 20484],
["L7*", 150, 21984],
["L8*", 155, 23784],
["L9*", 160, 25984],
["L10*", 165, 28584],
["L11*", 170, 31684],
["L12*", 175, 35384],
["L13*", 180, 39784],
["L14*", 185, 44984],
["L15*", 200, 51084],
["L16*", 205, 58284],
["L17*", 210, 61284],
["L18*", 215, 64524],
["L19*", 220, 68024],
["L20*", 230, 71804],
["L21*", 235, 75894],
["L22*", 240, 80314],
["L23*", 245, 85084],
["L24*", 250, 90224],
["L25*", 260, 95724]]

gi=3
for g in gemprop:
    g.append(gemprop.index(g))

g12=[]
for g1 in gemprop:
    for g2 in gemprop:
        g12.append([g1[gi], g2[gi], g1[1]+g2[1], g1[2]+g2[2]])

tl=2
gc=3

def getKeyTL(item):
    return item[tl]

def getKeyGC(item):
    return item[gc]

g12s=sorted(g12, key=getKeyGC)

g12ss=[]
low=g12s[0]
max=low[tl]
for gg in g12s:
    if (gg[tl]>max):
        if (g12s.index(low) != g12s.index(gg)-1):
            g12ss.append(sorted(g12s[g12s.index(low):g12s.index(gg)], key=getKeyGC))
        else:
            g12ss.append([low])
        low=gg
        max=low[tl]

if (g12s.index(low) != g12s.index(gg)-1):
    g12ss.append(sorted(g12s[g12s.index(low):], key=getKeyGC))
else:
    g12ss.append([low])

for o in g12ss:
    oo=o[0]
    print gemprop[oo[0]][0], gemprop[oo[1]][0], oo[2], oo[3]

for o in g12ss:
    ref_tl=o[0][tl]
    ref_gc=o[0][gc]
    for oo in o:
        oo.append(oo[tl]-ref_tl)
        oo.append(oo[gc]-ref_gc)

