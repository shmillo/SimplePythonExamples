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
    return zeroXing, np.array(indexXing)

def frequencyChange(x):
    return 2.0 * np.log(x)

def F(x, f):
    return np.sin(np.pi * 2.0 * f * x, dtype=np.float32)

sampleRate = 44100.0; dt = 1.0 / sampleRate

start = 0.0; stop = 0.5; step = 1.0/sampleRate; numSamples = int(sampleRate * (stop - start)) + 1
xAxis = np.arange(start, stop + step, step); yAxis = np.arange(start, stop + step, step)

numberOfSeconds = stop; simulationLengthInSamples = numSamples
sineSweepData = np.zeros( simulationLengthInSamples ); actualFrequencyArr = np.zeros( simulationLengthInSamples )

startFrequency = 1.0; endFrequency = 1000.0
T = numberOfSeconds; TWOPI = np.pi * 2.0
tempOne = TWOPI * startFrequency * T; tempTwo = TWOPI * endFrequency * T
tempThree = np.log( tempTwo / tempOne ); tempFour = tempOne / tempThree

time = 0.0
for i in range( 0, simulationLengthInSamples ):
    actualFrequencyArr[ i ] = np.exp((time / T) * tempThree)
    sineSweepData[ i ] = np.sin( tempFour * (np.exp((time / T) * tempThree) - 1.0) )
    time += dt

zeroXArr, indexArr = zerocrossingArray(sineSweepData)

indexArr = indexArr[2::2]; indexArr = np.insert(indexArr, 0, 0.0, axis=0); sampleRateArr = np.ones(indexArr.shape[0] - 1) * 44100.0; 
fundamentalFrequencyGuess = sampleRateArr / ((indexArr[1:] - indexArr[:-1]) + 0.5) 

print(indexArr, 'guesses =', fundamentalFrequencyGuess, 'actual =', actualFrequencyArr[indexArr])

fig, (ax1, ax2, ax3) = mplt.subplots(3)
ax1.plot(xAxis, sineSweepData); ax1.scatter(xAxis, zeroXArr-1.0, s=100.0*zeroXArr, c='r')
ax2.plot(fundamentalFrequencyGuess, label='guesses'); ax2.plot(actualFrequencyArr[indexArr], label='actual'); ax2.legend()
ax3.plot(actualFrequencyArr[indexArr[:-1]], np.sqrt((actualFrequencyArr[indexArr[:-1]] - fundamentalFrequencyGuess)**2.0), label='error'); ax3.legend()
mplt.show()