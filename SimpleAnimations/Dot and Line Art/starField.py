import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

class Star():
    global width, height

    def __init__(self):
        self.x = normalizeScalar(np.random.rand(), 0.0, 1.0, -width, width)
        self.y = normalizeScalar(np.random.rand(), 0.0, 1.0, -height, height)
        self.z = normalizeScalar(np.random.rand(), 0.0, 1.0, 0.0, width)
        self.sx = 0.0; self.sy = 0.0; self.size = 0.0

    def update(self):
        self.z = self.z - 1.0
        if(self.z < 1.0):
            self.z = width
            self.x = normalizeScalar(np.random.rand(), 0.0, 1.0, -width, width)
            self.y = normalizeScalar(np.random.rand(), 0.0, 1.0, -height, height)

    def show(self):
        self.sx = normalizeScalar(self.x/self.z, 0.0, 1.0, 0.0, width)
        self.sy = normalizeScalar(self.y/self.z, 0.0, 1.0, 0.0, width)
        self.size = normalizeScalar(self.z, 0.0, width, 16.0, 0.0 )
        return self.sx, self.sy, self.size

def normalizeVector(values, lowerDes, upperDes, lowerAct, upperAct):
    return [lowerDes + (x - lowerAct) * (upperDes - lowerDes) / (upperAct - lowerAct) for x in values]

def normalizeScalar(value, lowerAct, upperAct, lowerDes, upperDes):
    return lowerDes + (value - lowerAct) * (upperDes - lowerDes) / (upperAct - lowerAct)
 
def animationFunc(i):
    global stars, coordinateArray, sizeArray

    for i in range(len(stars)):
        coordinateArray[0][i], coordinateArray[1][i], sizeArray[0][i] = stars[i].show()
        stars[i].update()
    
    ax1.clear(); ax1.axis('off'); ax1.set_xlim([-width, width]); ax1.set_ylim([-height, height])
    ax1.scatter(coordinateArray[0], coordinateArray[1], s=sizeArray, color='w')

height = 100; width = 100; step = 1
xAxis = np.arange(-width, width + step, step); yAxis = np.arange(-height, height + step, step); X,Y = np.meshgrid(xAxis, yAxis)

stars = []; totalNumStars = 75
for i in range(totalNumStars):
    stars.append(Star())
coordinateArray = np.zeros([2, len(stars)])
sizeArray = np.zeros([1, len(stars)])

fig, ax1 = mplt.subplots(1, facecolor="black", dpi=300); fig.tight_layout(pad=0); ax1.axis('off') 
anim = FuncAnimation(fig, func=animationFunc, frames=np.linspace(0,100,num=100), interval=1)
anim.save('starField_T1.gif')
mplt.show()