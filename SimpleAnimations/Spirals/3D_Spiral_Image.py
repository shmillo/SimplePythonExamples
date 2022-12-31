import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation as fa

def gaussian(a, b, x):
    return (1.0/np.sqrt(2.0*np.pi*b)) * np.exp(-0.5*(1.0/b)*((x-a)**2.0))

fig, ax = mplt.subplots(1,1); ax = fig.add_subplot(projection='3d'); fig.set_size_inches(3.5, 3.5)
ax.set_xlim([-4, 4]); ax.set_ylim([-4, 4])
ax.azim = 0; ax.dist = 10; ax.elev = -90

def spiralFunc(i):
    global a, volumeDelta, numSpirals, numPointsPerFrame, totalNumFrames, zIndexIncrement
    for q in range(numSpirals):
        xdat = []; ydat = []; zdat = []
        zIndex = 0; 
        for j in range(int(i) - numPointsPerFrame, int(i)):
            constantOne = 2.0 * np.pi * (j/(totalNumFrames))
            xdat.append( a * np.cos(constantOne) + (0.005 * np.random.rand()) )
            ydat.append( a * np.sin(constantOne) + (0.005 * np.random.rand()) )
            zdat.append( 1.0 * (gaussian(1.195, 1.95, zIndex) + (0.05 * np.random.rand())) )
            a += volumeDelta; zIndex += zIndexIncrement
    ax.scatter(xdat, ydat, zdat, s=0.4)

totalNumFrames = 10000; numPointsPerFrame = 5000
a = 0.0; maximumArcRadius = 1.0; volumeDelta = maximumArcRadius/(numPointsPerFrame)
numSpirals = 1; zIndexIncrement = 5.0/numPointsPerFrame
ani = fa(fig, func=spiralFunc, frames=totalNumFrames, interval=10)
mplt.axis('off')
mplt.show()