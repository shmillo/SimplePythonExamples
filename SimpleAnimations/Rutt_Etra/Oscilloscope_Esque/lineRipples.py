from matplotlib.animation import FuncAnimation
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as mplt
import math
import numpy as np

def setAudioBuffer(audioData, tempBuffer, overlap, currentSample):
    global remainingSamples

    tempBuffer[:overlap] = tempBuffer[tempBuffer.shape[0] - overlap:]
    
    writeStart = overlap + 1; writeEnd = tempBuffer.shape[0]
    readStart = currentSample + overlap; readEnd = currentSample + overlap + remainingSamples; readDistance = (readEnd - readStart)

    if(readEnd > audioData.shape[0]):
        readEnd = audioData.shape[0]; readDistance = readEnd - readStart; writeEnd = writeStart + readDistance
        if(readDistance <= 0):
            tempBuffer[writeStart:] = 0.0
        else:
            tempBuffer[writeStart:writeEnd] = audioData[readStart:readEnd]
            tempBuffer[writeEnd:] = 0.0
    else:
        tempBuffer[writeStart:writeStart+readDistance] = audioData[readStart:readEnd]

def rms(X, frameLength, hopLength):

    rms = []
    for i in range(0, len(X), hopLength):
        rmsCurrent = np.sqrt( np.sum(X[i:i + frameLength]**2.0) / frameLength )
        rms.append(rmsCurrent)

    return rms

def animFunc(i):
    global audioDataSnare, audioTempBufferSnare, audioDataKick, audioTempBufferKick, overlapSize, currentSample, y, x

    ax.clear()
    ax.axis('off'); ax.set_xlim([-4.0, 4.0]); ax.set_ylim([-4.0, 4.0]); ax.set_facecolor('black')
    
    setAudioBuffer(audioDataSnare, audioTempBufferSnare, overlapSize, currentSample)
    heightValueSnare = (y - 1.0 + (audioTempBufferSnare))
    ax.scatter(x, heightValueSnare, s=1.0, c='g')

    setAudioBuffer(audioDataKick, audioTempBufferKick, overlapSize, currentSample)
    heightValueKick = (y - 3.0 + (audioTempBufferKick))
    ax.scatter(x, heightValueKick, s=1.0, c='g')

    setAudioBuffer(audioDataHat, audioTempBufferHat, overlapSize, currentSample)
    heightValueHat = (y + 1.0 + (audioTempBufferHat))
    ax.scatter(x, heightValueHat, s=1.0, c='g')

    currentSample += sampleIncrement

SAMPLERATE, audioDataSnare = wavfile.read("/Users/shawnmilloway/Downloads/snare_iso.wav")
audioDataSnare = np.array(audioDataSnare[:, 0], dtype=np.float32); print('audioData shape', audioDataSnare.shape)
audioDataSnare /= audioDataSnare.max(); audioDataRMS = np.array(rms(audioDataSnare, 256, 128)); print('audioDataRMS shape', audioDataRMS.shape)
#audioDataSnare = np.copy(audioDataRMS)

SAMPLERATE, audioDataKick = wavfile.read("/Users/shawnmilloway/Downloads/kick_iso.wav")
audioDataKick = np.array(audioDataKick[:, 0], dtype=np.float32); print('audioData shape', audioDataKick.shape)
audioDataKick /= audioDataKick.max(); audioDataRMSKick = np.array(rms(audioDataKick, 256, 128)); print('audioDataRMSKick shape', audioDataRMSKick.shape)
#audioDataKick = np.copy(audioDataRMSKick[:audioDataSnare.shape[0]])
audioDataKick = audioDataKick[:audioDataSnare.shape[0]]

SAMPLERATE, audioDataHat = wavfile.read("/Users/shawnmilloway/Downloads/hat_iso.wav")
audioDataHat = np.array(audioDataHat[:, 0], dtype=np.float32); print('audioData shape', audioDataHat.shape)
audioDataHat /= audioDataHat.max(); audioDataRMSHat = np.array(rms(audioDataHat, 256, 128)); print('audioDataRMSHat shape', audioDataRMSHat.shape)
#audioDataKick = np.copy(audioDataRMSKick[:audioDataSnare.shape[0]])
audioDataRMSHat = audioDataRMSHat[:audioDataSnare.shape[0]]

resolution = 3000.0
x = np.arange(-4.0, 4.0, (1.0/resolution)); y = np.ones([x.shape[0]], dtype=np.float32)
audioTempBufferSnare = np.zeros_like(x); audioTempBufferKick = np.zeros_like(x); audioTempBufferHat = np.zeros_like(x)

skewOne = x.shape[0]//2; skewTwo = x.shape[0] - skewOne
revealShape = np.concatenate( (np.linspace(0.0, 0.99, num=skewOne), np.linspace(0.99, 0.0, num=skewTwo)) ) 

fig, ax = mplt.subplots(1); fig.tight_layout(pad=0); fig.set_facecolor('black')
ax.axis('off'); ax.set_xlim([-4.0, 4.0]); ax.set_ylim([-4.0, 4.0]); ax.set_facecolor('black')

currentSample = 0; percentOverlap = 1.51; overlapSize = int(x.shape[0]/percentOverlap); sampleIncrement = (audioTempBufferSnare.shape[0] - overlapSize)
remainingSamples = audioTempBufferSnare.shape[0] - overlapSize - 1; numberOfSteps = int( audioDataSnare.shape[0]/sampleIncrement )

print(sampleIncrement, numberOfSteps)
anim = FuncAnimation(fig, func=animFunc, frames=range(numberOfSteps), interval=1)
anim.save("linesScope.gif", fps=30)
#mplt.show()
