import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

def anim_Func(i):
    global xgrid, ygrid, j, k, h, totalIts, sizeCount

    xscan = xgrid[h:h+sizeCount]; yscan = ygrid[j:j+sizeCount]; Z = fZ[j:j+sizeCount]

    j+=1
    if(j >= xgrid.shape[1]):
        j -= j
        k += 1
        if(k >= ygrid.shape[1]):
            k -= k
    h += 1
    if(h >= xgrid.shape[0]):
        h -= h

    sizeCount += 1
    if(sizeCount >= 40):
        sizeCount = 1

    totalIts += 1; refreshRate = 10
    if(totalIts >= refreshRate):
        ax.clear(); ax.set_xlim([-2.0, 2.0]); ax.set_ylim([-2.0, 2.0])
    ax.scatter(xscan, yscan, s=30.0*Z, cmap='ocean')

uB = 2.0; lB = -2.0; step = 0.1
xAxis = np.arange(lB, uB, step); yAxis = np.arange(lB, uB, step)
xgrid, ygrid = np.meshgrid(xAxis, yAxis)

#fZ = np.random.rand(xgrid.shape[0],xgrid.shape[1])*xgrid**2.0 + np.random.rand(xgrid.shape[0],xgrid.shape[1])*ygrid**2.0
fZ = np.random.rand(xgrid.shape[0],xgrid.shape[1])*np.sin(xgrid**2.0) + np.random.rand(xgrid.shape[0],xgrid.shape[1])*np.sin(ygrid**2.0)


fig, ax = mplt.subplots(1)
j = 0; k = 0; h = 0; totalIts = 8; sizeCount = 0; totalNumFrames = 80
animFunction = FuncAnimation(fig, func=anim_Func, frames = np.linspace(0, totalNumFrames, num=totalNumFrames), interval=1)
animFunction.save("scan_noise2.gif")
mplt.show()