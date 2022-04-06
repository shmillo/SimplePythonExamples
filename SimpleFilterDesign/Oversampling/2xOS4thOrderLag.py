from cmath import pi, sin, tanh
import matplotlib.pyplot as mplt

def processingFunction(x):

    val = x
    if(x > 1.0):
        val = 1.0
    elif(x < -1.0):
        val = -1.0

    return val

def lag(x, yn1, y0, y1, y2):

    z = x - 0.5 
    even1 = yn1 + y2; odd1 = yn1 - y2
    even2 = y0 + y1; odd2 = y0 - y1

    c0 = ((9/16) * even2) - ((1/16)*even1)
    c1 = ((1/24) * odd1) - ((9/8) * odd2)
    c2 = ((1/4) * (even1 - even2))
    c3 = (0.5 * odd2 - ((1/6) * odd1))
		
    return ((c3 * z + c2) * z + c1) * z + c0


sampleRate = 44100.0
dt = 1.0 / sampleRate

durationInSeconds = 0.009
durationInSamples = int( durationInSeconds * sampleRate )

interpolationOrder = 4
upSamplingRatio = 2
decimationScalar = 1.0 / upSamplingRatio

upMatrix = [0.0] * interpolationOrder
downMatrix = [ [0.0] * interpolationOrder for _ in range(upSamplingRatio - 1) ]

inputData = [0.0] * durationInSamples
controlData = [0.0] * durationInSamples
outputData = [0.0] * durationInSamples

t = 0.0
f = 1000.0
d1 = 0.0
for i in range(durationInSamples):

    inputData[i] = 15.0 * sin(2.0 * pi * t * f).real
    t += dt

    controlData[i] = processingFunction( inputData[i])

    upMatrix[3] = inputData[i]
    downMatrix[0][0] = processingFunction( inputData[i] )

    d2 = lag( 0.5, downMatrix[0][0], downMatrix[0][1], downMatrix[0][2], downMatrix[0][3] )
    outputData[i] = decimationScalar * (d1 + d2)
    d1 = processingFunction(lag( 0.5, upMatrix[0], upMatrix[1], upMatrix[2], upMatrix[3] ))
    
    for j in range(interpolationOrder - 1):
        upMatrix[j] = upMatrix[j + 1]

    for q in range(upSamplingRatio - 1):
        for h in range(interpolationOrder - 1, 0, -1):
            downMatrix[q][h] = downMatrix[q][h - 1]



fig, (ax1, ax2, ax3) = mplt.subplots(3)

ax1.plot(inputData)
ax2.plot(outputData)
ax3.plot(controlData)

mplt.show()
