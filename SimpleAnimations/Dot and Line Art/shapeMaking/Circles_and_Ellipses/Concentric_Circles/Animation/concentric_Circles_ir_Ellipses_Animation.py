import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

def animFunc(i):
    global timeVaryingCircles, timeStep, numTimeSteps, totalNumFrames, speed
    index = timeStep%numTimeSteps
    ax.clear(); ax.axis('off')
    ax.scatter(timeVaryingCircles[index][0].T, timeVaryingCircles[index][1].T, color='k', s=0.1)
    timeStep += speed

beginning = -5.0; end = -1.0 * beginning; step = 0.25
xAxis = np.arange(beginning, end, step); yAxis = np.arange(beginning, end, step); X, Y = np.meshgrid(xAxis,yAxis)

########### Initialize Arrays and outline a single radius #############
#######################################################################

numPoints = 200.0; numCircles = 100
circleArray = np.zeros([2, numCircles, int(numPoints)]); diameterArray = np.zeros([2, numCircles, int(numPoints)])

radialIncrement = (np.pi*2.0)/(numPoints - 1); radiusIncrementArray = np.arange(0, numPoints*radialIncrement, radialIncrement)

################ Determine Diameter Arrays ############################
#######################################################################

minDiameter = 0.10; maxDiameter = 4.0; diameterInc = (maxDiameter - minDiameter)/numCircles
diameterList = np.arange(minDiameter, maxDiameter, diameterInc)
for i in range(2):
    for j in range(numCircles):
        diameterArray[i][j] = (diameterList[j])

totalNumFrames = 100; speed = 2
numTimeSteps = int(totalNumFrames/speed); timeStep = 0; yRangePath = np.linspace(20, 0, num=numTimeSteps); print(yRangePath)
timeVaryingCircles = np.zeros([numTimeSteps, 2, numCircles, int(numPoints)]); print(timeVaryingCircles.shape)
for i in range(numTimeSteps):

    startingX = 0.0; endingX = 0.0
    if( (endingX - startingX) != 0.0 ):
        xPathList = (np.linspace(startingX, endingX, num=int(numCircles)))
    elif( (endingX - startingX) == 0.0 ):
        xPathList = np.zeros(int(numCircles)); xPathList[:] = startingX

    startingY = yRangePath[i]; endingY = -1.0*yRangePath[i]
    if( (endingY - startingY) != 0.0 ):
        yPathList = (np.linspace(startingY, endingY, num=int(numCircles)))
    elif( (endingY - startingY) == 0.0 ):
        yPathList = np.zeros(int(numCircles)); yPathList[:] = startingY

    pathArray = np.zeros([2, numCircles, int(numPoints)])
    for j in range(numCircles):
        pathArray[0][j][:] = xPathList[j]; pathArray[1][j][:] = yPathList[j]

    #######################################################################
    #######################################################################

    circleArray[0] = diameterArray[0] * np.cos(radiusIncrementArray) + np.cos(pathArray[0])
    circleArray[1] = diameterArray[1] * np.sin(radiusIncrementArray) + np.cos(pathArray[1])

    timeVaryingCircles[i][0] = circleArray[0]; timeVaryingCircles[i][1] = circleArray[1]

    #######################################################################
    #######################################################################

fig = mplt.figure(); ax = fig.add_subplot(); mplt.tight_layout(pad=0); ax.axis('off') #; ax.azim = -45; ax.elev(45)
anim = FuncAnimation(fig, func=animFunc, frames=np.linspace(0, totalNumFrames, num=totalNumFrames), interval=1)
anim.save("water_Ripple_travelling.gif")
mplt.show()