from cmath import exp, pi, sin
from re import I
import matplotlib.pyplot as mplt

def FFT(P):

    n = len(P)

    if n == 1:
        return P

    else:
        w = exp((2.0 * pi * I) / n)


        Pe = []
        Po = []
        for i in range(0, n, 2):
            Pe.append(P[ i ])
        for i in range(1, n, 2):
            Po.append(P[ i ])

        ye = FFT(Pe)
        yo = FFT(Po)

        y = [0.0] * n
        for j in range(int(n * 0.5)):
            y[j] = ye[j] + (w**j)*yo[j]
            y[j + int(n/2)] = ye[j] - (w**j)*yo[j]

    return y

def iFFT(P):

    n = len(P)

    if n == 1:
        return P

    else:
        w = exp((-2.0 * pi * I) / n)


        Pe = []
        Po = []
        for i in range(0, n, 2):
            Pe.append(P[ i ])
        for i in range(1, n, 2):
            Po.append(P[ i ])

        ye = iFFT(Pe)
        yo = iFFT(Po)

        y = [0.0] * n
        for j in range(int(n * 0.5)):
            y[j] = ye[j] + (w**j)*yo[j]
            y[j + int(n/2)] = ye[j] - (w**j)*yo[j]

    return y

#must be a power of 2
size = 256
testData = []

SAMPLERATE = 44100.0
dt = 1.0/SAMPLERATE

f = 1.0/(size/SAMPLERATE)
time = 0.0
for i in range(size):

    testData.append( sin(2.0 * pi * f * time).real + sin(2.0 * pi * 2.0 * f * time).real )

    time += dt

fftData = FFT(testData)

##### DO SOMETHING WITH FFT DATA #####


##### DO SOMETHING WITH FFT DATA #####

ifftData = iFFT(fftData)

for q in range( len(ifftData ) ):
    ifftData[q] /= size


fig, (ax1, ax2, ax3) = mplt.subplots(3)

ax1.plot( testData, label = 'original' )
ax2.plot( ifftData, label = 'reconstructed' )
ax3.plot( fftData, label = 'FFT' )

ax1.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )
ax2.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )
ax3.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

mplt.show()