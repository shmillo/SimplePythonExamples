
import importlib
from math import pi, sin
import matplotlib.pyplot as mplt

sampleRate = 44100.0
dt = 1.0/sampleRate

f = 30
numberOfPeriods = 3
lengthOfSample = numberOfPeriods * int( (1.0/f) * sampleRate )

totalTime = 8.0 * lengthOfSample
lengthOfWindow = int( totalTime )

######## ######## ######## ######## ######## ########

testDataOriginal = [ 0.0 ] * lengthOfWindow 
testDataCopy = [ 0.0 ] * lengthOfWindow 
autoCorrelation = [0.0] * lengthOfWindow

######## ######## ######## ######## ######## ########

offset = int( 0.5 * lengthOfWindow )
time = 0.0
for i in range( lengthOfSample ):
    testDataOriginal[ i + offset ] = sin( 2.0 * pi * f * time )
    time += dt

######## ######## ######## ######## ######## ########

beginning = int( 0.12 * lengthOfWindow )

numberOfIterations = 4
delayIncrement = int( (lengthOfWindow - beginning) / numberOfIterations )
totalDelaySize = int( delayIncrement * numberOfIterations )

startingPoint = beginning + delayIncrement
endingPoint = totalDelaySize + delayIncrement

######## ######## ######## ######## ######## ########

fig, (ax1, ax2, ax3) = mplt.subplots(3, sharex = True, sharey = True)
mplt.axis([ 0, lengthOfWindow, -1.0, 1.0 ])

######## ######## ######## ######## ######## ########

for i in range( startingPoint, endingPoint, delayIncrement ):

    for x in range( lengthOfSample ):
        
        if i + x < lengthOfWindow:

            testDataCopy[ i + x ] = testDataOriginal[ x + offset ]
            autoCorrelation[ i + x ] += testDataCopy[ i + x ] * testDataOriginal[ i + x ]

    ax2.plot( testDataCopy )
    ax3.plot( testDataOriginal )

######## ######## ######## ######## ######## ########

ax1.plot( autoCorrelation )

######## ######## ######## ######## ######## ########

mplt.show()
