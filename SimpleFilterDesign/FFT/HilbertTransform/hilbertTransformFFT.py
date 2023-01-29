import math
import numpy as np
from cmath import exp, pi, sin
import matplotlib.pyplot as mplt

def decibelNormalization(inputData, reference):
    return (10 * np.log10(np.abs(inputData)/reference))

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

    return y

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

    return np.array(y)


n = 2**8
randomNumbers = np.random.rand(n,1)
f = np.array( FFT(randomNumbers) ); complexF = 1j * f

#excludes the first element of each half
positiveFrequencyComponentIndexes = list(range(1, n//2 + n%2, 1))
negativeFrequencyComponentIndexes = list(range((math.ceil(n/2) + ~n%2), n, 1))

f[positiveFrequencyComponentIndexes] += -1j*complexF[positiveFrequencyComponentIndexes]
f[negativeFrequencyComponentIndexes] += 1j*complexF[negativeFrequencyComponentIndexes]

hilbertInverse = iFFT(f)/n

# set 0 dB to energy of sine wave with maximum amplitude
ref = (1/np.sqrt(2)**2)   

mplt.plot(decibelNormalization(hilbertInverse, hilbertInverse.max()))
mplt.show()
