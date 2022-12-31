import numpy as np
import matplotlib.pyplot as mplt

def F(x):
    return np.sin(np.pi * 2.0 * 11.7650 * x, dtype=np.float32)

def CMNDF(f, W, t, lag):
    if(lag == 0):
        return 1.0
    return DF(f, W, t, lag) / np.sum([DF(f, W, t, j+1) for j in range(lag)]) * lag 

def autoCorrelation(f, W, t, lag):
    return np.sum( f[t : (t + W)] * f[(lag + t) : (lag + t + W)] )

def DF(f, W, t, lag):
    return autoCorrelation(f, W, t, 0) + autoCorrelation(f, W, t + lag, 0) - (2.0 * autoCorrelation(f, W, t, lag)) 

def memoCMNDF(f, W, t, lag_max):
    running_sum = 0
    vals = []
    for lag in range(0, lag_max):
        if lag == 0:
            vals.append(1)
            running_sum += 0
        else:
            running_sum += DF(f, W, t, lag)
            vals.append(DF(f, W, t, lag) / running_sum * lag)
    return vals

def pitchDetectionThreshCMNDFAugmented(f, W, t, sampleRate, bounds, thresh=0.1):
    CMNDFvals = memoCMNDF(f, W, t, bounds[-1])[bounds[0]:]
    sample = None
    for i, val in enumerate(CMNDFvals):
        if val < thresh:
            sample = i + bounds[0]
            break
    if sample is None:
        sample = np.argmin(CMNDFvals) + bounds[0]
    return sampleRate / (sample + 1)

def pitchDetectionThreshCMNDF(f, W, t, sampleRate, bounds, thresh=0.1):
    CMNDFVals = np.array([CMNDF(f, W, t, i) for i in range(*bounds)], dtype=np.float32)
    sample = None
    for i, val in enumerate(CMNDFVals):
        if( val < thresh):
            sample = i + bounds[0]
            break
    if(sample is None):
        sample = np.argmin(CMNDFVals[bounds[0]:bounds[1]]) + bounds[0]
    return sampleRate/(sample + 1)

def pitchDetectionCMNDF(f, W, t, sampleRate, bounds):
    CMNDFVals = np.array([CMNDF(f, W, t, i) for i in range(*bounds)], dtype=np.float32)
    sample = np.argmin(CMNDFVals[bounds[0]:bounds[1]]) + bounds[0]
    return sampleRate/sample

def pitchDetectionDF(f, W, t, sampleRate, bounds):
    dFVals = np.array([DF(f, W, t, i) for i in range(*bounds)], dtype=np.float32)
    sample = np.argmin(dFVals[bounds[0]:bounds[1]]) + bounds[0]
    return sampleRate/sample

def pitchDetection(f, W, t, sampleRate, bounds):
    ACFValues = [autoCorrelation(f, W, t, i) for i in range(*bounds)]
    sample = np.argmax(ACFValues[bounds[0]:bounds[1]]) + bounds[0]
    return sampleRate/sample

sampleRate = 44100
start = 0; stop = 3; numSamples = int(sampleRate * (stop - start)) + 1
print('numSamples =', numSamples, 'lowerBound =', sampleRate/(numSamples//20), 'upperBound =', sampleRate/5)
windowSize = 200; bounds = [5, (numSamples//20)]
x = np.linspace(start, stop, numSamples, dtype=np.float32)
signal = F(x)

print( pitchDetection(F(x), windowSize, 1, sampleRate, bounds) )
print( pitchDetectionDF(F(x), windowSize, 1, sampleRate, bounds) )
print( pitchDetectionThreshCMNDF(F(x), windowSize, 1, sampleRate, bounds) )
print( pitchDetectionThreshCMNDFAugmented(F(x), windowSize, 1, sampleRate, bounds) )

