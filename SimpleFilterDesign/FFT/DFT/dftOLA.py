import math
import numpy as np
import matplotlib.pyplot as mplt

def naiveDFT(x):
    N = np.size(x)
    X = np.zeros((N,), dtype=np.complex128)
    for m in range(N):    
        for n in range(N): 
            X[m] += x[n] * np.exp(-np.pi*2j*m*n/N)
    return X

def naiveIDFT(x):
    N = np.size(x)
    X = np.zeros((N,), dtype=np.complex128)
    for m in range(N):
        for n in range(N): 
            X[m] += x[n] * np.exp(np.pi*2j*m*n/N)
    return X/N

def F(x):
    return np.sin(2.0 * np.pi * 100.0 * x)

sampleRate = 44100
start = 0; end = 0.3; numSamples = int((end - start) * sampleRate) + 1; step = 1.0/sampleRate
time = np.linspace(start, end, numSamples); print(time.shape[0])

signal = F(time)

Nx = numSamples; M = 16; N = 8 * 2**(math.ceil(np.log2(M))); print(N)
padSize = M - 1; stepSize = N - padSize; print('stepSize =', stepSize); zeroPad = np.zeros(padSize,)

numberOfBlocks = math.floor(Nx / stepSize); position = 0

outputData = np.zeros(Nx)
for _ in range(numberOfBlocks):

    writeStart = position
    writeEnd = position + N
    if(writeEnd > Nx):
        writeEnd = Nx - 1

    readStart = writeStart
    readEnd = writeEnd - padSize

    position += stepSize
    
    paddedSignal = np.concatenate((signal[readStart:readEnd], zeroPad))
    outputData[writeStart:writeEnd] = outputData[writeStart:writeEnd] + naiveIDFT(naiveDFT(paddedSignal))

mplt.plot(outputData)
mplt.show()
