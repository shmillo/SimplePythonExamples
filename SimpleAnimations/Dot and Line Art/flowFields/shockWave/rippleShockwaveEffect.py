import numpy as np
import matplotlib.pyplot as mplt

def normalizeVector(values, lowerAct, upperAct, lowerDes, upperDes):
  return np.array([lowerDes + (x - lowerAct) * (upperDes - lowerDes) / (upperAct - lowerAct) for x in values])

def normalizeScalar(value, lowerAct, upperAct, lowerDes, upperDes):
  return lowerDes + (value - lowerAct) * (upperDes - lowerDes) / (upperAct - lowerAct)

displayWidth = 100; displayHeight = 100; step = 1
xAxis = np.arange(0, displayWidth, step); yAxis = np.arange(0, displayHeight, step); X, Y = np.meshgrid(xAxis, yAxis)
xLimits = (-20.0, 20.0); yLimits = (-20.0, 20.0)

circumferenceLength = 50; rotationAxis = np.arange(0, (2.0*np.pi) + (2.0*np.pi)/circumferenceLength, (2.0*np.pi)/circumferenceLength)
cosScalar = np.cos(rotationAxis); sinScalar = np.sin(rotationAxis)
xRotation = cosScalar - sinScalar; yRotation = sinScalar + cosScalar

lengthInSeconds = 0.01; sampleRate = 44100; dt = 1.0/sampleRate; numSamples = int(lengthInSeconds * sampleRate); print(numSamples)
dampedAsymmetricSinusoid = np.zeros(numSamples); expMod = np.zeros(numSamples); ampEnv = np.zeros(numSamples); 

time = 0.0; nPeriods = 2.0; f = nPeriods/lengthInSeconds; maxDisplacement = 1.30; minDisplacement = 0.9
for i in range(numSamples):
    ampEnv[i] = np.exp(-5000.01 * time); 
    dampedAsymmetricSinusoid[i] = 1.0 + (ampEnv[i] * np.sin(np.pi * f * time)); time += dt

normalizedAsymmetricEnvelope = normalizeVector(dampedAsymmetricSinusoid, dampedAsymmetricSinusoid.min(), dampedAsymmetricSinusoid.max(), 0.9, 1.5)

numberOfCircles = 10; minDiameter = 1.0; maxDiameter = 10.0; spacingStep = maxDiameter/numberOfCircles
diameterArray = np.arange(minDiameter, maxDiameter + spacingStep, spacingStep)

totalTime = numberOfCircles*numSamples; logDelayTimes = np.logspace(1.0, 2.0, num=numberOfCircles, endpoint=True); 
logDelayTimes /= logDelayTimes.min(); logDelayTimes -= 1; logDelayTimes /= logDelayTimes.max(); np.sort(logDelayTimes)
logDelayTimes *= (numSamples - 5 - 1)/numberOfCircles; print(logDelayTimes)

xRotTemp = np.zeros([totalTime, len(rotationAxis)]); yRotTemp = np.zeros([totalTime, len(rotationAxis)])
xRotTemp[:] = xRotation; yRotTemp[:] = yRotation

displacementArray = np.zeros([2, numberOfCircles, len(rotationAxis), totalTime]); checkArray = np.zeros([numberOfCircles, numSamples])
for i in range(numberOfCircles):

    startingPoint = int(logDelayTimes[i]); endingPoint = startingPoint + numSamples

    displacementArray[0, i, :, :] = xRotTemp.T * diameterArray[i]
    displacementArray[1, i, :, :] = yRotTemp.T * diameterArray[i] 

    displacementArray[0, i, :, startingPoint:endingPoint] *= normalizedAsymmetricEnvelope
    displacementArray[1, i, :, startingPoint:endingPoint] *= normalizedAsymmetricEnvelope

    normalizedAsymmetricEnvelope = normalizeVector(dampedAsymmetricSinusoid, dampedAsymmetricSinusoid.min(), dampedAsymmetricSinusoid.max(), 1.0, max(1.00001, maxDisplacement))
    maxDisplacement *= 0.959

    checkArray[i] = normalizedAsymmetricEnvelope

for i in range(totalTime):
    mplt.xlim(xLimits); mplt.ylim(yLimits)
    for j in range(numberOfCircles):
        mplt.plot(displacementArray[0, j, :, i], displacementArray[1, j, :, i], color='k')
    mplt.draw()
    mplt.pause(0.000001)
    mplt.cla()

mplt.show()