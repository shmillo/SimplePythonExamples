from cmath import log, pi
from math import sin
import matplotlib.pyplot as mplt

def iterativeHaar(data):

    nSamples = len(data)

    nSweeps = int(log(nSamples).real / log(2.0).real)
    print(nSweeps)

    i = 1; gap = 2
    s = 0; d = 0 
    for j in range(1, nSweeps + 1):

        nSamples = int(nSamples * 0.5)

        for k in range(nSamples):

            s = (data[gap*k] + data[gap*k + i]) * 0.5
            d = (data[gap*k] - data[gap*k + i]) * 0.5

            data[gap*k] = s
            data[gap*k + i] = d

        i = gap
        gap *= 2

    return data

def inverseIterativeHaar(data):

    nSamples = len(data)

    nSweeps = int(log(nSamples).real / log(2.0).real)
    gap = int(2.0**(nSweeps - 1))

    jump = 2 * gap
    numFreqs = 1

    for i in range(nSweeps, 0, -1):
        for k in range(numFreqs):
            sums = data[jump*k] + data[jump*k + gap]
            diffs = data[jump*k] - data[jump*k + gap]
            data[jump*k] = sums
            data[jump*k + gap] = diffs
        jump = gap
        gap = int(gap * 0.5)
        numFreqs = int(numFreqs * 2)

    return data

###### ###### ###### ###### ###### ###### 
###### ###### ###### ###### ###### ###### 

sampleRate = 44100.0
dt = 1.0 / sampleRate

numSeconds = 0.1
simulationLengthInSamples = int( 256 )

fig, ( ax1, ax2, ax3 ) = mplt.subplots(3)

###### ###### ###### ###### ###### ###### 
###### ###### ###### ###### ###### ###### 

f = 300
time = 0.0
sineData = [0.0] * simulationLengthInSamples
for i in range(simulationLengthInSamples):
    sineData[i] = sin(2.0 * pi * f * time).real + sin(2.0 * pi * 2.0 * f * time).real
    time += dt

ax1.plot( sineData, label = 'Input Signal' )
ax1.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

###### ###### ###### ###### ###### ###### 

haarData = iterativeHaar(sineData)
ax2.plot( haarData, 's', label = 'Haar Coefficients' )
ax2.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

###### ###### ###### ###### ###### ###### 

reconstructedData = inverseIterativeHaar(haarData)
ax3.plot( reconstructedData, label = 'Reconstructed Data' )
ax3.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

###### ###### ###### ###### ###### ###### 

mplt.show()