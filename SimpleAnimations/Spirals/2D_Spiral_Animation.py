import numpy as np
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

fig, ax = mplt.subplots(1,1); ax.set_xlim([-2, 2]); ax.set_ylim([-2, 2])

def animation_frame(i):
    global offset, j

    numPointsRendered = 3000; totalNumFrames = 10000
    dimensionlessAxis = np.arange(int(i + offset) - numPointsRendered, int(i + offset), 1.0)   
    temporaryConstantOne = 2.0 * np.pi * (dimensionlessAxis/totalNumFrames)
    temporaryConstantTwo = (2.0*(i/totalNumFrames))
    xdat = temporaryConstantTwo * np.cos( temporaryConstantOne ) 
    ydat = temporaryConstantTwo * np.sin( temporaryConstantOne ) 
  
    if(i/totalNumFrames >= 0.33):
        dimensionlessAxis = np.arange(int(i + offset) - numPointsRendered, int(i + offset), 1.0)   
        temporaryConstantOne = 2.0 * np.pi * (dimensionlessAxis/totalNumFrames)
        temporaryConstantTwo = (2.0*(j/1000)); j+=50
        ydat2 = temporaryConstantTwo * np.cos( -1.0 * temporaryConstantOne )
        xdat2 = temporaryConstantTwo * np.sin( -1.0 * temporaryConstantOne )

        xdat = np.append(xdat, xdat2)
        ydat = np.append(ydat, ydat2)

    mplt.scatter(xdat, ydat, s=0.1) 

offset = 20000.0; j = 0.0
animation = FuncAnimation(fig, func=animation_frame, frames=np.linspace(0, 20000), interval=1)
#animation.save('increasingStraightLine.gif')
mplt.show()

