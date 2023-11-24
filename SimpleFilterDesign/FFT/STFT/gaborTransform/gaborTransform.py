from cmath import cos, exp, log, pi, sin, sqrt
import matplotlib.pyplot as mplt
import numpy as np

def nearestPow2(v):
  #print(v)
  v -= 1
  v |= v >> 1
  v |= v >> 2
  v |= v >> 4
  v |= v >> 8
  v |= v >> 16
  v += 1
  #print(v)
  return v
  
def rms(X, frameLength, hopLength):
    rms = []
    for i in range(0, len(X), hopLength):
        rmsCurrent = np.sqrt( np.sum(X[i:i + frameLength]**2.0) / frameLength )
        rms.append(rmsCurrent)
    return rms
    
def nearestPow2(v):
  #print(v)
  v -= 1
  v |= v >> 1
  v |= v >> 2
  v |= v >> 4
  v |= v >> 8
  v |= v >> 16
  v += 1
  #print(v)
  return v
 
def FFT(P):
    n = len(P)
    if n == 1:
        return P
    else:
        w = exp((2.0 * pi * 1.0j) / n)
        Pe = []
        Po = []
        for i in range(0, n, 2):
            Pe.append(P[ i ])
        for i in range(1, n, 2):
            Po.append(P[ i ])
        ye = FFT(Pe)
        yo = FFT(Po)
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
        Pe = []
        Po = []
        for i in range(0, n, 2):
            Pe.append(P[ i ])
        for i in range(1, n, 2):
            Po.append(P[ i ])
        ye = iFFT(Pe)
        yo = iFFT(Po)
        y = [0.0] * n
        for q in range(int(n * 0.5)):
            y[q] = ye[q] + (w**q)*yo[q]
            y[q + int(n/2)] = ye[q] - (w**q)*yo[q]
    return y

fig, ax = mplt.subplots(figsize = (6, 6))

SAMPLERATE = 44100.0; dt = 1.0/SAMPLERATE
numSamps = 2**12; print("numSamps ", numSamps)
frameTimeline = np.array(list(range(numSamps)))

sf = 22000; stheta = 0; numberOfVoices = 8; numberOfNoteChangeEvents = 10
timelineSignal = np.array([dt*i for i in range(0, numSamps)])

frequencyModifier = np.random.rand(numberOfVoices, numberOfNoteChangeEvents); magnitudeModifier = np.random.rand(numberOfVoices, numberOfNoteChangeEvents)

noteChangeTimes = np.array(numSamps * np.random.rand(numberOfVoices, numberOfNoteChangeEvents - 1), dtype=np.int64)
noteChangeTimes = np.array(np.append(noteChangeTimes, np.zeros([numberOfVoices, 1], dtype=np.int64), axis=1), dtype=np.int64)
noteChangeTimes.sort()
#print(noteChangeTimes)

tempSignal = np.zeros(numSamps)
for i in range(numberOfVoices):
    for j in range(numberOfNoteChangeEvents - 1):
        beginPoint = noteChangeTimes[i, j]; endPoint = noteChangeTimes[i, j+1]
        tempSignal[beginPoint:endPoint] += magnitudeModifier[i,j] * np.sin(2.0 * np.pi * (sf*frequencyModifier[i,j]) * timelineSignal[beginPoint:endPoint])
signal = tempSignal
signal = signal[:numSamps]
#mplt.plot(signal)

numFrames = 6
lengthOfFrames = int(numSamps/numFrames); print("lenghtOfFrames ", lengthOfFrames)
nP2 = nearestPow2(lengthOfFrames)

binFrequencies = [0.0] * lengthOfFrames
for u in range( lengthOfFrames ):
    binFrequencies[u] = ((u*SAMPLERATE)/lengthOfFrames)
binFrequencies = np.array(binFrequencies)
#print(binFrequencies)

frameData = np.zeros([numFrames, lengthOfFrames]); print(frameData.shape[1])
transformData = np.zeros([numFrames, lengthOfFrames]); magnitudes = np.zeros([numFrames, lengthOfFrames])

timeLineGaussian = np.linspace(-1.9143, 1.9143, lengthOfFrames)
ga = 10.005; gaussian = np.exp(-ga * timeLineGaussian**2)

hashGrid = np.zeros([lengthOfFrames*numFrames, lengthOfFrames])
for frame in range(numFrames):
  frameStartPointSamples = (frame*lengthOfFrames)
  frameEndPointSamples = (((frame + 1)*lengthOfFrames))
  frameData[frame] = signal[frameStartPointSamples:frameEndPointSamples]
  
  fftTempData = np.array(np.hstack((gaussian * frameData[frame], np.zeros(nP2 - lengthOfFrames))))
  transformData[frame] = np.array(np.hstack((FFT(fftTempData)[:lengthOfFrames//2], np.zeros(lengthOfFrames//2, dtype=np.cdouble))), dtype=np.cdouble)
  
  magnitudes[frame] = np.sqrt(transformData[frame].real**2 + transformData[frame].imag**2)
  #magnitudes[frame] /= magnitudes[frame].max()

  hashGrid[frameStartPointSamples:frameEndPointSamples, ::-1] = magnitudes[frame]
#displayFrames = np.hstack(frameData[:])

mplt.tight_layout(pad=0); mplt.yticks(fontsize=7)
#ax.set_yticks(list(range(1, lengthOfFrames, 100)), labels=binFrequencies[::100])
ax.set_yticks(list(range(1, lengthOfFrames//2, 50)), labels=np.int64(binFrequencies[:lengthOfFrames//2][::50]))
im = ax.imshow(hashGrid.T, extent=[0, numSamps, 0, lengthOfFrames//2], cmap='hot', vmin=0, vmax=magnitudes.max())

mplt.show()