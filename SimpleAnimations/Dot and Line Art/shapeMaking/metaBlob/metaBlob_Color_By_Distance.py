import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

class Blob():
    def __init__(self):
        self.posX = np.random.rand(); self.posY = np.random.rand()
        self.yVelocity = 1.0/(50.0 + np.random.rand()*10.0); self.xVelocity = self.yVelocity = 1.0/(50.0)

    def updatePosition(self):

        self.posX += self.xVelocity 
        if(self.posX >= 1.0 or self.posX <= 0.0):
            self.xVelocity *= -1.0
            self.posX += self.xVelocity

        self.posY += self.yVelocity
        if(self.posY >= 1.0 or self.posY <= 0.0):
            self.yVelocity *= -1.0
            self.posY += self.yVelocity 

        return self.posX, self.posY

def dist(x1, y1, x2, y2):
    returnValue = np.sqrt((x2 - x1)**2.0 + (y2 - y1)**2.0)
    return returnValue

def animFunc(i):
    global blobArr, sumX, sumY, colorArr, step, gridWidth, gridHeight, colorX, colorY, widthAxis, heightAxis
    
    ax1.clear(); ax1.set_xlim([0.0, gridWidth]); ax1.set_ylim([0.0, gridHeight])
    dx = gridWidth/(len(widthAxis - 1)); dy = gridHeight/(len(heightAxis) - 1)
    dt = 0.5/dy*dx; colorArr *= 0.5807; 

    blobPosArr = np.zeros([2, numBlobs])
    for j in range(numBlobs):
        blobPosArr[0][j], blobPosArr[1][j]  = blobArr[j].updatePosition()
    
    #sumX = 0.0; sumY = 0.0
    #sumY *= 0.33
    for x in range(1, len(widthAxis) - 1):
        #sumX *= 0.001
        for y in range(1, len(heightAxis) - 1):
            sumX = 0.0; sumY = 0.0 #sumY *= 0.753; sumX *= 0.753 
            for j in range(numBlobs):
                gwX = gridWidth * blobPosArr[0][j]; ghY = gridHeight * blobPosArr[1][j]
                val = 1.0/(dist(widthAxis[x], heightAxis[y], gwX, ghY) + 1.0e-6)
                sumX += val; sumY += val
            colorArr[x][y] += (sumX + sumY) + dt*(colorArr[x+1][y] + colorArr[x][y+1] - 4.0*colorArr[x][y] + colorArr[x][y-1] + colorArr[x-1][y])
    #ax1.scatter(gridWidth * blobPosArr[0], gridHeight * blobPosArr[1])
    ax1.scatter(colorX, colorY, c=colorArr)

numBlobs = 10; blobArr = []
for i in range(numBlobs):
    blobArr.append(Blob())

gridHeight = 10.0; gridWidth = 10.0; step = 0.1; sumX = 0.0; sumY = 0.0
widthAxis = np.arange(0, gridWidth, step); heightAxis = np.arange(0, gridHeight, step)
colorX, colorY = np.meshgrid(widthAxis, heightAxis); colorArr = np.zeros([colorX.shape[0], colorX.shape[1]])

fig, (ax1) = mplt.subplots(1); ax1.set_xlim([0.0, gridWidth]); ax1.set_ylim([0.0, gridHeight])
anim = FuncAnimation(fig, func=animFunc, frames=np.linspace(0, 100, num=100), interval=1)
anim.save("blob_spatial_Averager.gif")
mplt.show()

