import numpy as np
import matplotlib.pyplot as mplt

def signum(x):
    returnValue = 0.0
    if(x > 0.0):
        returnValue = 1.0
    elif(x < 0.0):
        returnValue = -1.0
    return returnValue

def zerocrossingCount(x):
    y = 0; l = len(x)
    for i in range(0, l-1):
        if( signum(x[i]) != signum(x[i+1]) ):
            y = y + 1
    return y

def zerocrossingArray(data):
    zeroXing = np.zeros_like(data); indexXing = []
    for i in range(len(data) - 1):
        if( signum(data[i]) != signum(data[i+1]) ):
            zeroXing[i] = 1.0; indexXing.append(i)
    return zeroXing, indexXing

def F(x):
    return np.sin(np.pi * 2.0 * 76.7650 * x, dtype=np.float32)

sampleRate = 44100; start = 0.0; stop = 0.2; numSamples = int(sampleRate * (stop - start)) + 1
xAxis = np.arange(start, stop, 1.0/sampleRate); yAxis = np.arange(start, stop, 1.0/sampleRate)
signal = F(xAxis); zeroXArr, indexArr = zerocrossingArray(signal)

fundamentalFrequencyGuess = sampleRate / (indexArr[2] + 0.5)
print(indexArr, fundamentalFrequencyGuess)

mplt.plot(xAxis, signal)
mplt.scatter(xAxis, zeroXArr-1.0, s=100.0*zeroXArr, c='r')
mplt.show()