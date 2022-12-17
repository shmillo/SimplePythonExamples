import numpy as np
import matplotlib.pyplot as mplt

class Star():
    global maxWeight, displayWidth, displayHeight
    
    def __init__(self):
        self.posX = np.random.rand() * displayWidth
        self.posY = np.random.rand() * displayHeight
        self.size = np.random.rand() * maxWeight
        self.color = (1.0 / maxWeight) * self.size
    
    def getPos(self):
        return self.posX, self.posY

        
maxWeight = 10.0; displayWidth = 100; displayHeight = 100; numStars = 400
step = 1
xAxis = np.arange(0, displayWidth, step); yAxis = np.arange(0, displayHeight, step); X, Y = np.meshgrid(xAxis, yAxis)

starArr = []; positionArray = np.zeros([2, numStars]); colorArr = np.zeros(numStars); sizeArr = np.zeros_like(colorArr)
for i in range(numStars):
    starArr.append(Star())
    positionArray[0][i], positionArray[1][i] = starArr[i].getPos()
    sizeArr[i] = starArr[i].size
    colorArr[i] = 1.0 - starArr[i].color; print(colorArr[i])


fig, ax = mplt.subplots(1); fig.tight_layout(pad=0); fig.set_facecolor('black'); ax.axis('off'); ax.set_facecolor('black')
ax.scatter(positionArray[0], positionArray[1], s=sizeArr, c=mplt.cm.Greys(colorArr))
mplt.show()
