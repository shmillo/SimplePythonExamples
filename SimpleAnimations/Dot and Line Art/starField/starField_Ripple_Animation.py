import math
import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

def normalizeVector(values, lowerAct, upperAct, lowerDes, upperDes):
  return np.array([lowerDes + (x - lowerAct) * (upperDes - lowerDes) / (upperAct - lowerAct) for x in values])

def normalizeScalar(value, lowerAct, upperAct, lowerDes, upperDes):
  return lowerDes + (value - lowerAct) * (upperDes - lowerDes) / (upperAct - lowerAct)

def angleAgainstXAxis(unitVector):
    return np.arctan2(unitVector[1], unitVector[0])

class Star():
    global maxWeight, displayWidth, displayHeight
    
    def __init__(self):
        self.posX = np.random.choice([-1.0, 1.0]) * np.random.rand() * displayWidth
        self.posY = np.random.choice([-1.0, 1.0]) * np.random.rand() * displayHeight
        self.size = np.random.rand() * maxWeight
        self.color = (1.0 / maxWeight) * self.size
    
    def getPos(self):
        return self.posX, self.posY

def animFunc(i):
    global displayWidth, displayHeight, starHashMap, rotationHashMap, timeCount

    ax.clear(); ax.set_facecolor('black'); ax.axis('off')
    ax.set_xlim([-displayWidth, displayWidth]); ax.set_ylim([-displayHeight, displayHeight])

    coords = starHashMap[0:2] + rotationHashMap[:, :, :, timeCount]; timeCount += 1
    ax.scatter(coords[0], coords[1], s=starHashMap[2], c=starHashMap[3], cmap='twilight')
    #mplt.scatter(rotationHashMap[0, :, :, i], rotationHashMap[1, :, :, i])

####################  ESTABLISH DISPLAY PARAMETERS ####################
#######################################################################

displayWidth = 100; displayHeight = 100; step = 1; count = 0
xAxis = np.linspace(-displayWidth, displayWidth, num=displayWidth*2); yAxis = np.linspace(-displayHeight, displayHeight, num=displayHeight*2); X, Y = np.meshgrid(xAxis, yAxis)
xLimits = (-20.0, 20.0); yLimits = (-20.0, 20.0)

#########  ESTABLISH COORDINATE ARRAYS FOR CONCENTRIC CIRCLES #########
#######################################################################

numberOfCircles = 20; minDiameter = 1.0; maxDiameter = displayWidth - 1; spacingStep = maxDiameter/numberOfCircles
diameterArray = np.arange(minDiameter, maxDiameter + spacingStep, spacingStep); diameterSquaredArray = diameterArray**2.0
coordinateArray = [[] for _ in range(numberOfCircles)]

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

angleArrayRadians = [[] for _ in range(numberOfCircles)]; angleArrayDegrees = [[] for _ in range(numberOfCircles)]
for i in range(numberOfCircles):
    for j in range(len(coordinateArray[i])):
        unitVector = np.array([float(coordinateArray[i][j][0]), float(coordinateArray[i][j][1])])
        norm = sum(unitVector**2.0)
        if(norm != 0.0):
            unitVector /= norm
        else:
            unitVector = [0.0, 0.0]
        angleArrayRadians[i].append(angleAgainstXAxis(unitVector))
        angleArrayDegrees[i].append(angleArrayRadians[i][j]*180.0/np.pi)

###################  ESTABLISH 2D Rotation Matrices ###################
#######################################################################

xRotation = [[] for _ in range(numberOfCircles)]; yRotation = [[] for _ in range(numberOfCircles)]
for i in range(numberOfCircles):
    rotationAxis = np.array(angleArrayRadians[i])
    cosScalar = np.cos(rotationAxis); sinScalar = np.sin(rotationAxis)
    xRotation[i].append(diameterArray[i] * (cosScalar - sinScalar))
    yRotation[i].append(diameterArray[i] * (sinScalar + cosScalar))

###############  ESTABLISH NORMALIZED ENVELOPE MATRICES ###############
#######################################################################

lengthInSeconds = 0.01; sampleRate = 44100; dt = 1.0/sampleRate; numSamples = int(lengthInSeconds * sampleRate); #print(numSamples)
dampedAsymmetricSinusoid = np.zeros(numSamples); expMod = np.zeros(numSamples); ampEnv = np.zeros(numSamples); 

time = 0.0; nPeriods = 2.0; f = nPeriods/lengthInSeconds
for i in range(numSamples):
    ampEnv[i] = np.exp(-5000.01 * time); 
    dampedAsymmetricSinusoid[i] = 1.0 + (ampEnv[i] * np.sin(np.pi * f * time)); time += dt

############  ESTABLISH DELAY TIMES FOR ENVELOPE MATRICES #############
#######################################################################

totalTime = 2*numSamples; logDelayTimes = np.logspace(1.0, 2.0, num=numberOfCircles, endpoint=True); 
logDelayTimes /= logDelayTimes.min(); logDelayTimes -= 1; logDelayTimes /= logDelayTimes.max(); np.sort(logDelayTimes)
logDelayTimes *= (numSamples - 5 - 1)/numberOfCircles

###############  FINALIZE NORMALIZED ENVELOPE MATRICES ################
#######################################################################

normalizedAsymmetricEnvelopes = np.ones([numberOfCircles, totalTime]);  maxDisplacement = 1.50; minDisplacement = 0.9
for i in range(numberOfCircles):
    startPoint = int(logDelayTimes[i]); endPoint = startPoint + numSamples
    normalizedAsymmetricEnvelopes[i, startPoint:endPoint] *= np.abs(normalizeVector(dampedAsymmetricSinusoid, dampedAsymmetricSinusoid.min(), dampedAsymmetricSinusoid.max(), 1.0, max(1.00001, maxDisplacement)))
    maxDisplacement *= 0.987

#####################  ESTABLISH ENVELOPE HASHMAP #####################
#######################################################################

rotationHashMap = np.ones([2, displayWidth*2, displayHeight*2, totalTime], dtype=np.float32)
for j in range(numberOfCircles):
    for i in range(len(coordinateArray[j])):
        rotationHashMap[0, coordinateArray[j][i][0]+displayWidth, coordinateArray[j][i][1]+displayHeight] *= np.ones_like(normalizedAsymmetricEnvelopes[j]) + (xRotation[j][0][i] * normalizedAsymmetricEnvelopes[j] * 20.0/displayWidth)
        rotationHashMap[1, coordinateArray[j][i][0]+displayWidth, coordinateArray[j][i][1]+displayHeight] *= np.ones_like(normalizedAsymmetricEnvelopes[j]) + (yRotation[j][0][i] * normalizedAsymmetricEnvelopes[j] * 20.0/displayWidth)

#######################  ESTABLISH STAR HASHMAP #######################
#######################################################################

maxWeight = 10.0; numStars = 300; step = 1
xAxis = np.arange(0, displayWidth, step); yAxis = np.arange(0, displayHeight, step); X, Y = np.meshgrid(xAxis, yAxis)
starHashMap = np.zeros([4, displayWidth*2, displayHeight*2])

starArr = []; positionArray = np.zeros([2, numStars]); colorArr = np.zeros(numStars); sizeArr = np.zeros_like(colorArr)
for i in range(numStars):

    starArr.append(Star())

    positionArray[0][i], positionArray[1][i] = starArr[i].getPos()
    hashMapXindex = math.floor(positionArray[0][i]) + displayWidth; hashMapYindex = math.floor(positionArray[1][i]) + displayHeight
    starHashMap[0:2, hashMapXindex, hashMapYindex] = positionArray[:, i]
    
    sizeArr[i] = starArr[i].size
    starHashMap[2, hashMapXindex, hashMapYindex] = sizeArr[i]
    
    colorArr[i] = 1.0 - starArr[i].color
    starHashMap[3, hashMapXindex, hashMapYindex] = colorArr[i]

####################  APPLY 2D DILATION OPERATION #####################
#######################################################################

fig, ax = mplt.subplots(1); fig.set_facecolor('black'); fig.tight_layout(pad=0); ax.set_facecolor('black'); ax.axis('off')

timeCount = 0

anim = FuncAnimation(fig, func=animFunc, frames=range(totalTime), interval=1)
anim.save("starFieldRipple.gif", fps=60)

#mplt.show()

