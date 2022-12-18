import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

class Star():
    global maxWeight, displayWidth, displayHeight, topSpeed, minSpeed
    
    def __init__(self):
        self.margin = 1 
        self.posX = np.random.rand() * displayWidth
        self.posY = np.random.rand() * displayHeight
        self.size = np.random.rand() * maxWeight
        self.speed = normalizeScalar(self.size, 0.0, maxWeight, minSpeed, topSpeed)
        self.color = (1.0 / maxWeight) * self.size
    
    def getPos(self):
        return self.posX, self.posY
    
    def movePos(self, directionX, directionY):
        
        self.posX += self.speed * directionX
        if(self.posX > displayWidth + self.margin):
            self.posX += -(displayHeight + self.margin)
        elif(self.posX < 0.0 - self.margin):
            self.posX += self.margin + displayHeight

        self.posY += self.speed * directionY
        if(self.posY > displayHeight + self.margin):
            self.posY += -(displayHeight + self.margin)
        elif(self.posY < 0.0 - self.margin):
            self.posY += displayHeight + self.margin

def normalizeScalar(value, lowerAct, upperAct, lowerDes, upperDes):
  return lowerDes + (value - lowerAct) * (upperDes - lowerDes) / (upperAct - lowerAct)

def updateAllStars():
    global directionX, directionY, numStars
    
    for i in range(numStars):
        starArr[i].movePos(directionX, directionY)
        positionArray[0][i], positionArray[1][i] = starArr[i].getPos()
        sizeArr[i] = starArr[i].size
        colorArr[i] = 1.0 - starArr[i].color

def onkey(event):
    global directionX, directionY, starArr, positionArray, sizeArr
    print(event.key)
    if event.key == 'f':
        directionX = -1.0; directionY = 0.0
    if(event.key == 'g'):
        directionX = 0.0; directionY = 0.0
    if event.key == 'h':
        directionX = 1.0; directionY = 0.0
    if(event.key == 't'):
        directionX = 0.0; directionY = 1.0
    if(event.key == 'y'):
        directionX = 1.0; directionY = 1.0
    if(event.key == 'r'):
        directionX = -1.0; directionY = 1.0
    
    print(directionX, directionY)

def onclick(event):
    global ax
    
    for i in range(100):
        updateAllStars()
        ax.clear(); ax.axis('off'); ax.set_facecolor('black'); ax.set_xlim([0, displayWidth]); ax.set_ylim([0, displayHeight])
        ax.scatter(positionArray[0], positionArray[1], s=sizeArr, c=mplt.cm.Greys(colorArr))
        mplt.draw()
        mplt.pause(0.05)

maxWeight = 10.0; displayWidth = 100; displayHeight = 100; numStars = 400; step = 1
directionX = 0.0; directionY = 0.0; minSpeed = 0.009; topSpeed = 1.50
xAxis = np.arange(0, displayWidth, step); yAxis = np.arange(0, displayHeight, step); X, Y = np.meshgrid(xAxis, yAxis)

starArr = []; positionArray = np.zeros([2, numStars]); colorArr = np.zeros(numStars); sizeArr = np.zeros_like(colorArr)
for i in range(numStars):
    starArr.append(Star())
    positionArray[0][i], positionArray[1][i] = starArr[i].getPos()
    sizeArr[i] = starArr[i].size
    colorArr[i] = 1.0 - starArr[i].color; print(colorArr[i])

fig, ax = mplt.subplots(1); fig.tight_layout(pad=0); fig.set_facecolor('black'); ax.axis('off'); ax.set_facecolor('black')
ax.set_xlim([0, displayWidth]); ax.set_ylim([0, displayHeight])
ax.scatter(positionArray[0], positionArray[1], s=sizeArr, c=mplt.cm.Greys(colorArr))

cid2 = fig.canvas.mpl_connect('key_press_event', onkey)
cid = fig.canvas.mpl_connect('button_press_event', onclick)

mplt.show(); mplt.draw()
