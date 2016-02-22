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
["L23*", 245, 85094],
["L24*", 250, 90264],
["L25*", 255, 95854],
["L26*", 260, 101894],
["L27*", 265, 108424],
["L28*", 270, 115484],
["L29*", 275, 123114],
["L30*", 290, 131364], # 8250 assumed
["L31*", 295, 140344], #
["L32*", 300, 149974], #
["L33*", 305, 160384], #
["L34*", 310, 171634], #
["L35*", 320, 183784], #
["L36*", 325, 196914], #
["L37*", 330, 211104], #
["L38*", 335, 226434], #
["L39*", 340, 242994], #
["L40*", 350, 260884], #
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

gl = [ "L14", "L5*", "L10*", "L15*", "L20*", "L25*", "L30*", "L35*", "L40*" ]
levels = []
ticks = []
labels = []
for i in gl:
    for g in gemprop:
        if (g[0] == i):
            if (g[2] < 200000): # exclude > 2 L40* contour
                levels.append(2*g[2])
                labels.append("{0}".format(levels[gl.index(i)])+" = 2 "+i )
            ticks.append(g[gi])

for g1, g2 in [ (14, 19), (24, 29) ]: #, (29, 34) ]:
    gsum = gemprop[g1][2] + gemprop[g2][2]
    prev = levels[0]
    for i in levels:
        if (i > gsum and prev < gsum):
            ii = levels.index(i)
            levels.insert(ii, gsum)
            labels.insert(ii, "{0}".format(gsum)+" = "+gemprop[g1][0]+" + "+gemprop[g2][0])
            break
        prev = i

opt = ( "optimum", "white" )
opt1k = ( "$\leqslant$ opt + 1024", (0.6, 1.0, 0.6) )
opt2k = ( "$\leqslant$ opt + 2048", (0.2, 1.0, 0.2) )
opt4k = ( "$\leqslant$ opt + 4096", (0.0, 0.7, 0.0) )
nonopt = ( "$>$ opt + 4096", (0.0, 0.4, 0.0) )
tl5 = ( "TL worse by  5", (0.0, 0.5, 1.0) )
tl10 = ( "TL worse by 10", (0.0, 0.0, 0.8) )
tl15 = ( "TL worse by 15", (0.5, 0.0, 0.2) )
tl20 = ( "TL worse by 20", (0.3, 0.0, 0.0) )
tl25 = ( "TL worse by 25", (0.2, 0.0, 0.0) )
tl30 = ( "TL worse by 30", (0.1, 0.0, 0.0) )
quality = [ opt, opt1k, opt2k, opt4k, nonopt, tl5, tl10, tl15, tl20 ] #, tl25, tl30 ]

ax = plt.gca()
for g in g12:
    c = None
    if (g[5] == 0):
        if (g[4] == 0):
            c = opt[1]
        elif (g[4] <= 1024):
            c = opt1k[1]
        elif (g[4] <= 2048):
            c = opt2k[1]
        elif (g[4] <= 4096):
            c = opt4k[1]
        else:
            c = nonopt[1]
    elif (g[5] <= 5):
        c = tl5[1]
    elif (g[5] <= 10):
        c = tl10[1]
    elif (g[5] <= 15):
        c = tl15[1]
    elif (g[5] <= 20):
        c = tl20[1]
    if (c):
        ax.add_patch(patches.Rectangle((g[0]-.5, g[1]-.5), 1., 1., color=c ))

oversample = 5
x = y = np.arange(-.5+.5/oversample, len(gemprop)-.5+.5/oversample, 1./oversample)
X, Y = np.meshgrid(x, y)
#DGC=np.empty_like(X)
#DTL=np.empty_like(X)
#TL=np.empty_like(X)
GC=np.empty_like(X)
for o in g12:
    for i in range(oversample*o[0], oversample*(o[0]+1)):
        for j in range(oversample*o[1], oversample*(o[1]+1)):
            GC[i][j] = o[gc]
            #TL[i][j] = o[tl]
            #DGC[i][j] = o[4]
            #DTL[i][j] = o[5]

#plt.imshow(np.minimum(DTL,20), interpolation='nearest'); plt.show()
#plt.imshow(np.minimum(DGC,8192), interpolation='nearest'); plt.show()

CS = plt.contour(X, Y, GC, levels, linewidths=2 )
artists = CS.legend_elements()[0]
plt.gca().add_artist(plt.legend(artists, labels, loc='upper right', bbox_to_anchor=(1.0, 1.0), mode="expand", frameon = False, fontsize="small"))

ax.annotate("gem cost less or equal to:", xy=(0,0), xytext=(1.025, 1.0), xycoords="axes fraction", fontsize="small")

# suggested optimal upgrades
opt_path = [[0], [0]]
for i in range(1, 15): # balanced to 2 L14
    opt_path[0].append(i); opt_path[1].append(i-1)
    opt_path[0].append(i); opt_path[1].append(i)
for i in range(16, 20): # L13 + L2* .. L5*
    opt_path[0].append(i); opt_path[1].append(13)
for i in range(13, 20): # to 2 L5*
    opt_path[0].append(19); opt_path[1].append(i)
for i in range(20, 25): # balanced to 2 L10*
    opt_path[0].append(i); opt_path[1].append(i-1)
    opt_path[0].append(i); opt_path[1].append(i)
for i in range(25, 30): # to L10* + L15*
    opt_path[0].append(i); opt_path[1].append(24)
for i in range(25, 30): # to 2 L15*
    opt_path[0].append(29); opt_path[1].append(i)
for i in range(30, 35): # to L15* + L20*
    opt_path[0].append(i); opt_path[1].append(29)
for i in range(30, 35): # to 2 L20*
    opt_path[0].append(34); opt_path[1].append(i)
for i in range(35, 40): # balanced  to 2 L25*
    opt_path[0].append(i); opt_path[1].append(i-1)
    opt_path[0].append(i); opt_path[1].append(i)
for i in range(40, 45): # to L25* + L30*
    opt_path[0].append(i); opt_path[1].append(39)
for i in range(40, 45): # to 2 L30*
    opt_path[0].append(44); opt_path[1].append(i)
for i in range(45, 50): # to L30* + L35*
    opt_path[0].append(i); opt_path[1].append(44)
for i in range(45, 50): # to 2 L35*
    opt_path[0].append(49); opt_path[1].append(i)
for i in range(50, 55): # to L35* + L40*
    opt_path[0].append(i); opt_path[1].append(49)
for i in range(50, 55): # to 2 L40*
    opt_path[0].append(54); opt_path[1].append(i)

#alternative paths
opt_path1 = [ [], [] ]
for i in range(29, 35): # to L10* + L20*
    opt_path1[0].append(i); opt_path1[1].append(24)
for i in range(25, 30): # to 2 L20*
    opt_path1[0].append(34); opt_path1[1].append(i)

opt_path2 = [ [], [] ]
for i in range(35, 40): # to L20* + L25*
    opt_path2[0].append(i); opt_path2[1].append(34)
for i in range(35, 40): # to 2 L25*
    opt_path2[0].append(39); opt_path2[1].append(i)

for op in [ opt_path ]: #, opt_path2 ]: #, opt_path1 ]:
    plt.plot(op[0], op[1], "r:", lw=2)
    plt.plot(op[0], op[1], "b.", lw=2)

plt.gca().add_artist(plt.legend((["suggested upgrade\npath for a pair of gems", ""]), loc='right', labelspacing=-1.5, bbox_to_anchor=(1.0, 0.5), mode="expand", frameon = False, fontsize="small"))
#ax.annotate("?", xy=(0,0), xytext=(.93, .93), xycoords="axes fraction", fontsize="large")

plt.ylabel("left gem")
plt.xlabel("right gem")
ll=10.5
hh=len(gemprop)-0.5
plt.axis([ll, hh, ll, hh])
plt.xticks(ticks, gl)
plt.yticks(ticks, gl)
ax.tick_params(direction='out', length=6, width=2)
ax.set_axis_bgcolor("black")
ax.set_aspect('equal', 'box', 'W')

rect = []
labels = []
for i in quality:
    rect.append(patches.Rectangle([0., 0.],1., 1., color=i[1]))
    labels.append(i[0])

plt.legend(rect, labels, loc='lower right', bbox_to_anchor=(1.0, -0.05), mode="expand", frameon = False, fontsize="small")

#plt.show()
plt.savefig("gem_build_opt.png", facecolor="silver")
