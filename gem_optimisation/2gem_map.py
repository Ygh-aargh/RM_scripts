#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# gem level name, treasure level, gem count
gemprop = [
["L0", 0, 0],
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
#["L24*", 250, 90224],
#["L25*", 260, 95724]
]

# gemprop[gi] = generalized gem level
gi = 3
for g in gemprop:
    g.append(gemprop.index(g))

# all gem combinations, a bit redundant but it is small array
g12 = []
for g1 in gemprop:
    for g2 in gemprop:
        g12.append([g1[gi], g2[gi], g1[1]+g2[1], g1[2]+g2[2]])

# g12[tl] = effective treasure level of 2 gems
# g12[gc] = sum of gem costs of 2 gems
tl = 2
gc = 3

# find lowest gem costs for given effective treasure levels
# some treasure levels are more costly than some higher ones
lg = {}
for gg in g12:
    if (gg[tl] in lg):
        if (lg[gg[tl]] > gg[gc]):
            lg[gg[tl]] = gg[gc]
    else:
        lg[gg[tl]] = gg[gc]

maxstep=0
for i in range(1, len(gemprop)-1):
    if (gemprop[i][1]-gemprop[i-1][1] > maxstep):
        maxstep = gemprop[i][1]-gemprop[i-1][1]
# maxstep = 20

# now remove unoptimal things
lg_opt = lg.copy()
for i in lg:
    for l in range(i-1, max(0, i-maxstep), -1):
        if (l in lg_opt):
            if (lg[l] > lg[i]):
                del lg_opt[l]

# determine how far it is in terms of used gems and treasure level
# very unoptimal implementation, use some sorting to have it faster
for gg in g12:
    dgc=0
    dtl=0
    for i in lg_opt:
        if (gg[tl] <= i):
            dgc = max(dgc, gg[gc]-lg_opt[i])
        if (gg[gc] >= lg_opt[i]):
            dtl = max(dtl, i-gg[tl])
    gg.append(dgc)
    gg.append(dtl)

x = y = np.arange(0, len(gemprop), 1)
X, Y = np.meshgrid(x, y)
DGC=np.empty_like(X)
DTL=np.empty_like(X)
TL=np.empty_like(X)
GC=np.empty_like(X)
for o in g12:
    GC[o[0]][o[1]] = o[gc]
    TL[o[0]][o[1]] = o[tl]
    DGC[o[0]][o[1]] = o[4]
    DTL[o[0]][o[1]] = o[5]

#plt.imshow(np.minimum(DTL,20), interpolation='nearest'); plt.show()
#plt.imshow(np.minimum(DGC,8192), interpolation='nearest'); plt.show()

gl = [ "L14", "L5*", "L10*", "L15*", "L20*" ]
levels = []
ticks = []
for i in gl:
    for g in gemprop:
        if (g[0] == i):
            levels.append(2*g[2])
            ticks.append(g[gi])

labels = []
for i in gl:
    labels.append("2 "+i+" = {0}".format(levels[gl.index(i)]))

g1 = 24
g2 = 29
gsum = gemprop[g1][2] + gemprop[g2][2]
prev = levels[0]
for i in levels:
    if (i > gsum and prev < gsum):
        ii = levels.index(i)
        levels.insert(ii, gsum)
        labels.insert(ii, gemprop[g1][0]+" + "+gemprop[g2][0]+" = {0}".format(gsum))
        break
    prev = i

quality = {
    "optimum": "white",
    "<= opt + 1024": (0.6, 1.0, 0.6),
    "<= opt + 2048": (0.2, 1.0, 0.2),
    "<= opt + 4096": (0.0, 0.7, 0.0),
    ">  opt + 4096": (0.0, 0.4, 0.0),
    "TL worse by  5": (0.0, 0.5, 1.0),
    "TL worse by 10": (0.0, 0.0, 0.8),
    "TL worse by 15": (0.5, 0.0, 0.2),
    "TL worse by 20": (0.3, 0.0, 0.0)
}

ax = plt.gca()
for g in g12:
    c = None
    if (g[5] == 0):
        if (g[4] == 0):
            c=quality["optimum"]
        elif (g[4] <= 1024):
            c=quality["<= opt + 1024"]
        elif (g[4] <= 2048):
            c=quality["<= opt + 2048"]
        elif (g[4] <= 4096):
            c=quality["<= opt + 4096"]
        else:
            c=quality[">  opt + 4096"]
    elif (g[5] <= 5):
        c=quality["TL worse by  5"]
    elif (g[5] <= 10):
        c=quality["TL worse by 10"]
    elif (g[5] <= 15):
        c=quality["TL worse by 15"]
    elif (g[5] <= 20):
        c=quality["TL worse by 20"]
    if (c):
        ax.add_patch(patches.Rectangle((g[0]-.5, g[1]-.5), 1., 1., color=c ))

CS = plt.contour(X, Y, GC, levels )
artists = CS.legend_elements()[0]
plt.gca().add_artist(plt.legend(artists, labels, loc='upper right', bbox_to_anchor=(1.0, 1.0), mode="expand", frameon = False, fontsize="small"))

ax.annotate("gem cost equal to:", xy=(0,0), xytext=(1.05, 1.0), xycoords="axes fraction")
plt.ylabel("left gem")
plt.xlabel("right gem")
plt.axis([10.5, 36.5, 10.5, 36.5])
plt.xticks(ticks, gl)
plt.yticks(ticks, gl)
ax.tick_params(direction='out', length=6, width=2)
ax.set_axis_bgcolor("black")
ax.set_aspect('equal', 'box', 'W')

rect = []
labels = []
for i in [ "optimum", "<= opt + 1024", "<= opt + 2048", "<= opt + 4096", ">  opt + 4096", "TL worse by  5", "TL worse by 10", "TL worse by 15", "TL worse by 20" ]:
    rect.append(patches.Rectangle([0., 0.],1., 1., color=quality[i]))
    labels.append(i)

plt.legend(rect, labels, loc='lower right', bbox_to_anchor=(1.0, 0.), mode="expand", frameon = False, fontsize="medium")

#plt.show()
plt.savefig("gem_build_opt.png", facecolor="silver")
