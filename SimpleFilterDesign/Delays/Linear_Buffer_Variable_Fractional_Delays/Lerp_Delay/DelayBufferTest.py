
from cmath import pi, sin
import matplotlib.pyplot as mplt

sampleRate = 44100.0
dt = 1.0 / sampleRate

simulationLengthSeconds = 0.1
simulationLengthSamples = int( simulationLengthSeconds * sampleRate )

testData = [0.0] * simulationLengthSamples
delayData = [0.0] * simulationLengthSamples
inputData = [0.0] * simulationLengthSamples
delayTimeData = [0.0] * simulationLengthSamples
fractionalDelayTimeData = [0.0] * simulationLengthSamples

frequency = 200.0
f = (frequency * sampleRate) / (simulationLengthSamples)


delayTimeSamples = ( simulationLengthSeconds * 0.05 ) * sampleRate
delayTimeSamplesInitial = delayTimeSamples

readPointerInt = int( delayTimeSamples )
readPointerFrac = delayTimeSamples - readPointerInt


time = 0.0
offset = 0
ramp = 0.0
for i in range(simulationLengthSamples):

    inputData[ i ] = sin (2.0 * pi * f * time )
    time += dt

    ########### ########### ########### ########### ########### ########### ###########
    ########### ########### ########### ########### ########### ########### ###########

    delayData[ i ] = ((1.0 - readPointerFrac) * testData[ readPointerInt ]) + (readPointerFrac * testData[ readPointerInt + (1 + offset) ])
    
    ########### ########### ########### ########### ########### ########### ###########
    ########### ########### ########### ########### ########### ########### ###########

    if i > delayTimeSamplesInitial * 1.5:
        delayTimeSamples += (0.9 * ramp)

    if ramp < 1.0:
        ramp = ramp + (0.0008 * (1.0 - ramp))

    if delayTimeSamples > simulationLengthSamples - 2:
        delayTimeSamples = simulationLengthSamples - 2

    readPointerInt = int( delayTimeSamples )
    readPointerFrac = delayTimeSamples - readPointerInt

    delayTimeData[ i ] = readPointerInt
    fractionalDelayTimeData[ i ] = delayData[ i ] + inputData[ i ]

    ########### ########### ########### ########### ########### ########### ###########
    ########### ########### ########### ########### ########### ########### ###########

    testData[ 0 ] = inputData[ i ]

    for q in range( simulationLengthSamples - 1, 0, -1 ):
        testData[ q ] = testData[ q - 1 ]

fig, (ax1, ax2, ax3, ax4, ax5) = mplt.subplots( 5, sharex = True )

ax1.plot(inputData)
ax2.plot(testData)
ax3.plot(delayData)
ax4.plot(delayTimeData)
ax5.plot(fractionalDelayTimeData)

mplt.show()