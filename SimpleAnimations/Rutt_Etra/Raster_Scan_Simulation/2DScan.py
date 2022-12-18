import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

def rasterAnimation(i):
    global X, Y, gridDepth, gridWidth, gridHeight, writeHeadHorizontal, writeHeadVertical, writeHeadArray, blurSize, memoryCount, trailLength, decayScaler

    ax.clear()
    ax.set_facecolor('black'); ax.set_xlim(-5, gridWidth + 5); ax.set_ylim(-5, gridHeight + 5); ax.set_zlim([0, 5]); ax.axis('off')
    
    ax.scatter(X[writeHeadHorizontal], Y[writeHeadHorizontal], zs=2.0*writeHeadArray[writeHeadHorizontal], zdir=X[writeHeadHorizontal], c='g')
    if(writeHeadHorizontal > 1):
        ax.scatter(X[0], Y[0], zs=2.0*interpFData[0], zdir=X[0], c='g', alpha = 0.5)
        if(writeHeadHorizontal >= gridWidth*0.25):
            idx = int(gridWidth*0.25)
            ax.scatter(X[idx], Y[idx], zs=2.0*interpFData[idx], zdir=X[idx], c='g', alpha = 0.5)
            if(writeHeadHorizontal >= gridWidth*0.5):
                idx = int(gridWidth*0.5)
                ax.scatter(X[idx], Y[idx], zs=2.0*interpFData[idx], zdir=X[idx], c='g', alpha = 0.5)
                if(writeHeadHorizontal >= gridWidth*0.75):
                    idx = int(gridWidth*0.75)
                    ax.scatter(X[idx], Y[idx], zs=2.0*interpFData[idx], zdir=X[idx], c='g', alpha = 0.5)

    writeHeadHorizontal += writeHeadStep
    if(writeHeadHorizontal >= gridWidth):
        writeHeadHorizontal -= writeHeadHorizontal
        wipeStart = int(gridWidth/1.05)
        writeHeadArray[wipeStart:] *= 0.0

    if(writeHeadHorizontal >= 0 and writeHeadHorizontal <= gridWidth - 1): 
        
        if(writeHeadHorizontal >= 1):
            wipeStart = writeHeadHorizontal - 1; wipeEnd = writeHeadHorizontal
            writeHeadArray[wipeStart:wipeEnd] = 0.0
        
        writeStart = writeHeadHorizontal; writeEnd = writeHeadHorizontal + 1
        writeHeadArray[writeStart:writeEnd] = interpFData[writeStart:writeEnd]

def bilinearInterpolationOnAnArray(x, y, lX, lY):
    
    fq11 = outputGrid[x[0]][y[0]]; fq12 = outputGrid[x[0]][y[1]]
    fq21 = outputGrid[x[1]][y[0]]; fq22 = outputGrid[x[1]][y[1]]
    
    tempOne = (1.0/((x[1] - x[0])*(y[1] - y[0]))) 
    tempTwo = x[1] - lX; tempThree = lX - x[0]
    tempFour = y[1] - lY; tempFive = lY - y[0]

    outVal = fq11 * tempTwo * tempFour
    outVal += fq21 * tempThree * tempFour
    outVal += fq12 * tempTwo * tempFive
    outVal += fq22 * tempThree * tempFive
    
    return outVal * tempOne

gridWidth = 500; gridHeight = 500; gridDepth = 10; resolution = 1; noiseAmount = 50
blurSize = 100.0; trailLength = 5; decayScaler = 0.2; memoryCount = 0; trailArr = np.zeros([2, trailLength], dtype=np.uint64)

xAxis = np.arange(0, gridWidth, resolution); yAxis = np.arange(0, gridHeight, resolution); zAxis = np.arange(0, gridDepth, resolution)
X, Y = np.meshgrid(xAxis, yAxis)

writeHeadHorizontal = 0; writeHeadVertical = 0; writeHeadStep = 1; writeHeadArray = np.zeros([gridWidth,gridHeight], dtype=np.float32); print(writeHeadArray.shape)

############################## CREATE 2D NOISE LUT FOR RASTER ############################## 
############################################################################################
 
nPoints = 10; nPointsM1 = 2
grid = np.zeros([nPoints, nPoints]); xCoordArray = np.arange(0, grid.shape[0], 1); yCoordArray = np.arange(0, grid.shape[1], 1)
numSteps = 50; step = 1.0/numSteps; xSubCoordArray = np.arange(0.0, nPoints, step); ySubCoordArray = np.arange(0.0, nPoints, step)

outputGrid = np.random.rand(nPoints + 1, nPoints + 1)

dimensionSize = nPoints*numSteps
interpXData = np.zeros([dimensionSize, dimensionSize]); interpYData = np.zeros([dimensionSize, dimensionSize]); interpFData = np.zeros([dimensionSize, dimensionSize])

currentXCoord = 0.0; currentYCoord = 0.0
for i in range(grid.shape[1] - 1):
  for j in range(grid.shape[0] - 1):
    for h in range(nPointsM1*numSteps):
      for k in range(nPointsM1*numSteps):
            axm = (j*numSteps) + k; aym = (i*numSteps) + h 
            currentXCoord = xCoordArray[j] + xSubCoordArray[k]
            currentYCoord = yCoordArray[i] + ySubCoordArray[h] 
            currentXArray = [xCoordArray[j], xCoordArray[j+1]]; currentYArray = [yCoordArray[i], yCoordArray[i+1]]
            interpXData[axm][aym] = currentXCoord; interpYData[axm][aym] = currentYCoord; interpFData[axm][aym] = bilinearInterpolationOnAnArray(currentXArray, currentYArray, currentXCoord, currentYCoord)

##################################### INITIALIZE PLOTS ##################################### 
############################################################################################
 
fig = mplt.figure(); fig.set_facecolor('black'); fig.tight_layout(pad=0); ax = fig.add_subplot(projection='3d')
ax.set_facecolor('black'); ax.axis('off'); ax.set_xlim(0, gridWidth); ax.set_ylim(0, gridHeight)

anim = FuncAnimation(fig, func=rasterAnimation, frames=range(500), interval=1)
anim.save('terrainOutline.gif', fps=30)
mplt.show()