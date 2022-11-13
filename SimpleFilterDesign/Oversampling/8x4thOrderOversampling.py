from cmath import pi, sin, tanh
import matplotlib.pyplot as mplt

def processingFunction(x):
    return tanh(x)

def fourthOrderLagrange(x, yn1, y0, y1, y2):

    z = x - 0.5
    
    even1 = yn1 + y2; odd1 = yn1 - y2
    even2 = y0 + y1; odd2 = y0 - y1

    c0 = ((9/16) * even2) - ((1/16)*even1)
    c1 = ((1/24) * odd1) - ((9/8) * odd2)
    c2 = ((1/4) * (even1 - even2))
    c3 = (0.5 * odd2 - ((1/6) * odd1 ))

    return (((c3 * z + c2) * z + c1) * z + c0)

############ ############ ############ ############
####### ############ ############ ############ ####
############ ############ ############ ############

sampleRate = 44100.0
dt = 1.0 / sampleRate

testDurationInSeconds = 0.01
testDurationInSamples = int( testDurationInSeconds * sampleRate )

sampleData = [0.0] * testDurationInSamples
controlData = [0.0] * testDurationInSamples
outputSamples = [0.0] * testDurationInSamples

upSamplingRatio = 8
interpolationOrder = 4

inputSamples = [0.0] * interpolationOrder
upwardInterpolatedSamps = [0.0] * upSamplingRatio
downwardInterpolatedSamps = [ [0.0] * interpolationOrder  for _ in range(upSamplingRatio - 1) ]

decimationScalar = 1.0 / upSamplingRatio

############ ############ ############ ############
####### ############ ############ ############ ####
############ ############ ############ ############

f = 4500.0
t = 0.0
histo = 0.0
testNumber = 0.0
for i in range(testDurationInSamples):

    sampleData[i] = 20.0 * sin( 2.0 * pi * f * t ).real
    t += dt
    
    controlData[i] = processingFunction( sampleData[i] )

    inputSamples[3] = sampleData[i]

    ############ ############ ############ ############

    fractionalDelay = decimationScalar
    for k in range( upSamplingRatio - 1 ):
        upwardInterpolatedSamps[k] = fourthOrderLagrange( fractionalDelay, inputSamples[0], inputSamples[1], inputSamples[2], inputSamples[3] )
        fractionalDelay += decimationScalar
    upwardInterpolatedSamps[upSamplingRatio - 1] = inputSamples[2]

    ############ ############ ############ ############

    outputTemp = processingFunction( histo )

    fractionalDelay = decimationScalar
    for g in range( 1, upSamplingRatio - 1 ):
        downwardInterpolatedSamps[g][0] = processingFunction( upwardInterpolatedSamps[g] )
        outputTemp += fourthOrderLagrange( fractionalDelay, downwardInterpolatedSamps[g][0], downwardInterpolatedSamps[g][1], downwardInterpolatedSamps[g][2], downwardInterpolatedSamps[g][3] )
        fractionalDelay += decimationScalar
    testNumber = fractionalDelay
    outputSamples[i] = outputTemp / 7.0

    ############ ############ ############ ############

    for j in range( 0, interpolationOrder - 1 ):
        inputSamples[j] =  inputSamples[j + 1]

    for d in range( 0, upSamplingRatio - 1 ):   
        for j in range( interpolationOrder - 1, 0, -1 ):
            downwardInterpolatedSamps[d][j] =  downwardInterpolatedSamps[d][j - 1]
    histo = upwardInterpolatedSamps[0]

############ ############ ############ ############
####### ############ ############ ########### #####
############ ############ ############ ############

fig, (ax1, ax2, ax3) = mplt.subplots(3)

ax1.plot(sampleData)
ax2.plot(outputSamples)
ax3.plot(controlData)

mplt.show()