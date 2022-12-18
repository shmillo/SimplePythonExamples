import numpy as np
import matplotlib.pyplot as plt


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

fig = plt.figure(figsize=(5,5)); fig.tight_layout(pad=0); ax = fig.add_subplot(projection='3d'); ax.axis('off')
ax.dist = 8; ax.azim = 45.0; ax.elev = -60.0

nPoints = 10; nPointsM1 = 2
grid = np.zeros([nPoints, nPoints]); xCoordArray = np.arange(0, grid.shape[0], 1); yCoordArray = np.arange(0, grid.shape[1], 1)
numSteps = 20; step = 1.0/numSteps; xSubCoordArray = np.arange(0.0, nPoints, step); ySubCoordArray = np.arange(0.0, nPoints, step)

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

ax.plot_surface(interpXData, interpYData, interpFData)
plt.show()



