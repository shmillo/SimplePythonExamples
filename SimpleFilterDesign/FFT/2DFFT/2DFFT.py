import numpy as np
from cmath import exp, pi, sin
import matplotlib.pyplot as mplt

def FFT(P):

    n = len(P)

    if n == 1:
        return P

    else:
        w = exp((2.0 * pi * 1.0j) / n)

        Pe = []; Po = []
        for i in range(0, n, 2):
            Pe.append(P[ i ])
        for i in range(1, n, 2):
            Po.append(P[ i ])

        ye = FFT(Pe); yo = FFT(Po)

        y = [0.0] * n
        for q in range(int(n * 0.5)):
            y[q] = ye[q] + (w**q)*yo[q]
            y[q + int(n/2)] = ye[q] - (w**q)*yo[q]

    return np.array( y )

def iFFT(P):

    n = len(P)

    if n == 1:
        return P

    else:
        w = exp((-2.0 * pi * 1.0j) / n)


        Pe = []; Po = []
        for i in range(0, n, 2):
            Pe.append(P[ i ])
        for i in range(1, n, 2):
            Po.append(P[ i ])

        ye = iFFT(Pe); yo = iFFT(Po)

        y = [0.0] * n
        for q in range(int(n * 0.5)):
            y[q] = ye[q] + (w**q)*yo[q]
            y[q + int(n/2)] = ye[q] - (w**q)*yo[q]

    return np.array( y )

def fftShift(fftData):
    
    height, width = fftData.shape
    halfWidth = width//2; halfHeight = height//2

    shifted = np.zeros_like(fftData)

    shifted[(height - halfHeight):height, (width - halfWidth):width] = fftData[:halfHeight, :halfWidth]
    shifted[(height - halfHeight):height, 0:(width - halfWidth)] = fftData[:halfHeight, halfWidth:width]
    shifted[0:(height - halfHeight), (width - halfWidth):width] = fftData[halfHeight:height, :halfWidth]
    shifted[0:(height - halfHeight), 0:(width - halfWidth)] = fftData[halfHeight:height, halfWidth:width]

    return shifted

fig, (ax1, ax2, ax3) = mplt.subplots(3)

signal = np.random.rand(256, 256)
ax1.contourf(signal, label='signal data')

twoDFFT = fftShift( FFT(FFT(signal).T) )
ax2.contourf(twoDFFT, label='FFT data')

iFFT2D = (iFFT( iFFT(fftShift(twoDFFT)).T )/(signal.shape[0]**2.0)).real
ax3.contourf(iFFT2D, label='reconstructed data')

mplt.show()



