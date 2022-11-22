import numpy as np
from matplotlib import transforms
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

fig, ax = mplt.subplots(1,1,figsize=(5, 5)); fig.tight_layout(pad=0)
ax.set_xlim([-4, 4]); ax.set_ylim([-4, 4])
ax.azim = 90; ax.dist = 3; ax.elev = 90
ax.axis('off'); ax.axis('square') 

def animation_frame(i):
    global offset, j, lines, iterationCount, numPointsRendered, totalNumFrames, rotationDegrees, rot, base

    dimensionlessAxis = np.arange(int(i + offset) - numPointsRendered, int(i + offset), 1.0)   
    temporaryConstantOne = 2.0 * np.pi * (dimensionlessAxis/totalNumFrames); temporaryConstantTwo = (2.0 * (i/totalNumFrames))
    xdat = temporaryConstantTwo * np.cos( temporaryConstantOne ); ydat = temporaryConstantTwo * np.sin( temporaryConstantOne ) 
    line, = ax.plot(xdat, ydat, color='k', transform = rot + base); lines.append(line) 
    iterationCount += 1

    rotationDegrees = (rotationDegrees + 10)%360
    rot = transforms.Affine2D().rotate_deg(rotationDegrees)
    base = mplt.gca().transData

    if(iterationCount >= 3):
        for line in lines[:2]:
            line.remove(); del line
        lines[:2] = []
        iterationCount = iterationCount - iterationCount

rotationDegrees = 0; rot = transforms.Affine2D().rotate_deg(rotationDegrees); base = mplt.gca().transData
offset = 100.0; j = 0.0; iterationCount = 0; numPointsRendered = 3000; totalNumFrames = 10000; lines = []
animation = FuncAnimation(fig, func=animation_frame, frames=np.linspace(0, 40000), interval=30)
animation.save('increasingStraightLine_Step_3.gif')
mplt.show()

