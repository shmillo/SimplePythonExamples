import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

class Blob():
    def __init__(self):
        self.posX = np.random.rand(); self.posY = np.random.rand()
        self.yVelocity = 1.0/(200.0 + np.random.rand()*100.0); self.xVelocity = self.yVelocity = 1.0/(200.0 + np.random.rand()*100.0)
        self.yVelocity *= np.random.choice([-1.0, 1.0]); self.xVelocity *= np.random.choice([-1.0, 1.0])

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
    global decayMod, blobArr, sumArr, colorArr, step, gridWidth, gridHeight, colorX, colorY, widthAxis, heightAxis
    
    #ax1.clear(); ax1.set_xlim([0.0, gridWidth]); ax1.set_ylim([0.0, gridHeight])
    
    blobPosArr = np.zeros([2, numBlobs]); oldBlobPosArr = np.zeros([2, numBlobs])
    oldBlobPosArr = blobPosArr
    for j in range(numBlobs):
        blobPosArr[0][j], blobPosArr[1][j] = blobArr[j].updatePosition()
    blobPosArr[0] *= gridWidth; blobPosArr[1] *= gridHeight

    sumArr *= decayMod; decayMod *= 0.99
    for x in range(1, len(widthAxis) - 2):
        for y in range(1, len(heightAxis) - 2):
            for j in range(numBlobs):
                val = 1.0/(dist(blobPosArr[0][j], blobPosArr[1][j], widthAxis[x], heightAxis[y]) + 1.0e-6)
                sumArr[x][y] += val
    
    #box blur
    #colorArr[begX:endX, begY:endY] = sumArr + 0.25*(colorArr[begX+1:endX+1, begY:endY] + colorArr[begX:endX,begY+1:endY+1] + colorArr[begX-1:endX-1, begY:endY] + colorArr[begX:endX, begY-1:endY-1])
    
    #gaussian blur 3x3
    colorArr[begX:endX, begY:endY] = sumArr + (1.0/16)*(4.0*colorArr[begX:endX, begY:endY] + 2.0*colorArr[begX+1:endX+1, begY:endY] + 2.0*colorArr[begX:endX,begY+1:endY+1] + 2.0*colorArr[begX-1:endX-1, begY:endY] + 2.0*colorArr[begX:endX, begY-1:endY-1] + colorArr[begX-1:endX-1, begY-1:endY-1] + colorArr[begX+1:endX+1, begY-1:endY-1] + colorArr[begX+1:endX+1, begY+1:endY+1] + colorArr[begX-1:endX-1, begY+1:endY+1])
    
    ax1.scatter(colorX, colorY, c=colorArr)

numBlobs = 5; blobArr = []
for i in range(numBlobs):
    blobArr.append(Blob())

gridHeight = 10.0; gridWidth = 10.0; step = 0.2; decayMod = 0.9
widthAxis = np.arange(0, gridWidth, step); heightAxis = np.arange(0, gridHeight, step)
colorX, colorY = np.meshgrid(widthAxis, heightAxis); colorArr = np.zeros([colorX.shape[0], colorX.shape[1]])
sumArr = np.zeros([colorArr.shape[0]-2,colorArr.shape[1]-2]); endX = colorArr.shape[0]-1; endY = colorArr.shape[1]-1; begX = 1; begY = 1

fig, (ax1) = mplt.subplots(1); ax1.set_xlim([0.0, gridWidth]); ax1.set_ylim([0.0, gridHeight])
anim = FuncAnimation(fig, func=animFunc, frames=np.linspace(0, 50, num=50), interval=1)
anim.save("blob_spatial_Averager_T4.gif")
#mplt.show()

