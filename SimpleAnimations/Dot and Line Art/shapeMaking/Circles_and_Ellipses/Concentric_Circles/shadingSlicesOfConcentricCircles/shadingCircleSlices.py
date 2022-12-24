import numpy as np
import matplotlib.pyplot as mplt

displayWidth = 50; displayHeight = 50; step = 1
xAxis = np.arange(0, displayWidth, step); yAxis = np.arange(0, displayHeight, step)

numberOfCircles = 20; minDiameter = 1.0; maxDiameter = displayWidth - 1; spacingStep = maxDiameter/numberOfCircles
diameterArray = np.arange(minDiameter, maxDiameter + spacingStep, spacingStep); diameterSquaredArray = diameterArray**2.0
coordinateArray = [[] for _ in range(numberOfCircles)]

fig, ax = mplt.subplots(1); ax.set_xlim([-displayWidth, displayWidth]); ax.set_ylim([-displayHeight, displayHeight])

for i in range(-displayWidth, displayWidth, 1):
    for j in range(-displayHeight, displayHeight, 1):
        checkValue = i**2.0 + j**2.0
        for d in range(numberOfCircles):
            if(checkValue <= diameterSquaredArray[d]):
                if(d > 0):
                    if(checkValue > diameterSquaredArray[d - 1]):
                        coordinateArray[d].append([i, j])
                else:
                    coordinateArray[d].append([i, j])

for i in range(numberOfCircles):
    coordinateSubArray = np.array(coordinateArray[i])
    mplt.scatter(coordinateSubArray.T[0], coordinateSubArray.T[1], cmap='prism')

mplt.show()