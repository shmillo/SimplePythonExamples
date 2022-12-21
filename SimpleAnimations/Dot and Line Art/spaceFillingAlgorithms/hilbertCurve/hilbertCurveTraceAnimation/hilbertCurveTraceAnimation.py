import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

def Hilbert(i):
    global points, order

    index = i&3
    v = np.array(points[index])
    for j in range(1, order):
        i = i >> 2
        index = i&3
        len = 2**j
        if(index == 0):
            temp = v[0]; v[0] = v[1]; v[1] = temp
        elif(index == 1):
            v[1] += len
        elif(index == 2):
            v[0] += len; v[1] += len
        elif(index == 3):
            temp = len - 1 - v[0]
            v[0] = len - 1 - v[1]
            v[1] = temp; v[0] += len
    return v;  

def lerp(v, p1, p2):
    return ((1.0 - v) * p1) + (v * p2)

def animFunc(i):
    global xCoords, yCoords, lerpVal, lerpStep, currentPoint, total
 
    lerpedXCoord[0] = xCoords[currentPoint]
    lerpedXCoord[1] = lerp(lerpVal, xCoords[currentPoint], xCoords[currentPoint + 1])
    
    lerpedYCoord[0] = yCoords[currentPoint]
    lerpedYCoord[1] = lerp(lerpVal, yCoords[currentPoint], yCoords[currentPoint + 1])

    lerpVal += lerpStep
    if(lerpVal > 1.0):
        lerpVal = 0
        currentPoint += 1
        if(currentPoint >= total - 1):
            currentPoint = 0
    
    ax.plot(lerpedXCoord, lerpedYCoord, color=mplt.cm.prism(lerpedYCoord[1]/(total-1)), linewidth=2.0)

fig, ax = mplt.subplots(1); fig.set_facecolor("black")

order = 4; N = int(2**order); total = N**2
points = np.zeros([4, 2]); points[0] = [0, 0]; points[1] = [0, 1]; points[2] = [1, 1]; points[3] = [1, 0]

width = 1; heighth = 1; len = width / N
xAxis = np.arange(100); yAxis = np.arange(100); X, Y = np.meshgrid(xAxis, yAxis)

path = np.zeros([total, 2]); xCoords = []; yCoords = []
for i in range(total):
    path[i] = Hilbert(i)
    xCoords.append(path[i][0]); yCoords.append(path[i][1])

lerpVal = 0.0; lerpStep = 0.3; currentPoint = 0; lerpedXCoord = [0.0] * 2; lerpedYCoord = [0.0] * 2

ax.set_xlim([-0.5, N]); ax.set_ylim([-0.5, N]); ax.set_facecolor("black")
anim = FuncAnimation(fig, func=animFunc, frames=range(1200), interval=1)
anim.save("hilbertTrace.gif")
mplt.show()