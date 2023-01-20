from matplotlib.animation import FuncAnimation
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as mplt
import numpy as np

def generateSawtooth(frequency, level, numTimeSteps):
    global PI, TWOPI, K, sawtooth
    
    sawtooth = np.zeros(numTimeSteps)
    f, q, l = 0.0, 0.0, 0.0
    for j in range(numTimeSteps):
    
        f += (frequency - f) / 4096.0; l = (level * 16384.0 - l) / 4096.0
        if(q < PI): 
            q += f * K
        else:
            q += (f * K) - TWOPI

        t = (q/PI) * l
        if(t < 0.0):
            t = 1.0 + t
        sawtooth[j] = t

    return sawtooth

def setAudioBuffer(audioData, overlap, currentSample):
    global remainingSamples, audioTempBuffer

    #print("audioTempBufferShape", audioTempBuffer.shape, audioData[currentSample:currentSample + overlap].shape)
    #print("currentSample", currentSample, "current + overlap", currentSample + overlap)
    #print(currentSample + overlap + 1, currentSample + overlap + 1 + remainingSamples, audioData[currentSample + overlap + 1:currentSample + overlap + 1 + remainingSamples].shape)
    #print( audioTempBuffer[overlap + 1:].shape )

    audioTempBuffer[:overlap] = audioTempBuffer[audioTempBuffer.shape[0] - overlap:]
    
    writeStart = overlap + 1; writeEnd = audioTempBuffer.shape[0]
    readStart = currentSample + overlap; readEnd = currentSample + overlap + remainingSamples; readDistance = (readEnd - readStart)

    if(readEnd > audioData.shape[0]):
        readEnd = audioData.shape[0]; readDistance = readEnd - readStart; writeEnd = writeStart + readDistance
        if(readDistance <= 0):
            audioTempBuffer[writeStart:] = 0.0
        else:
            audioTempBuffer[writeStart:writeEnd] = audioData[readStart:readEnd]
            audioTempBuffer[writeEnd:] = 0.0
    else:
        audioTempBuffer[writeStart:writeStart+readDistance] = audioData[readStart:readEnd]

def rms(X, frameLength, hopLength):

    rms = []
    for i in range(0, len(X), hopLength):
        rmsCurrent = np.sqrt( np.sum(X[i:i + frameLength]**2.0) / frameLength )
        rms.append(rmsCurrent)

    return rms

def animFunc(i):
    global xAngle, yAngle, audioTempBuffer, currentSample, sampleIncrement, idx, sawtoothLen
    
    ax.clear(); ax.axis('off'); ax.set_xlim([-2.0, 2.0]); ax.set_ylim([-2.0, 2.0]); ax.set_facecolor('black')

    setAudioBuffer(audioData, overlapSize, currentSample); currentSample += sampleIncrement

    plotX = (xAngle * (1.0 - sawtooth[idx])); plotY = ((yAngle + (2.0*audioTempBuffer - 1.0)) * (1.0 - sawtooth[idx]))
    ax.scatter(plotX, plotY, s=0.5, alpha=audioTempBuffer, c='green')

    idx = (idx + 1)%sawtoothLen

#/Users/shawnmilloway/Desktop/EP_Zen/EOIK_voice_phrase1.wav
#/Users/shawnmilloway/Downloads/Redetachment_Fame_Impala_Snippet_final.wav
SAMPLERATE, audioData = wavfile.read("/Users/shawnmilloway/Desktop/EP_Zen/EOIK_voice_phrase1.wav")
audioData = np.array(audioData, dtype=np.float32); print('audioData shape', audioData.shape)
audioData /= audioData.max(); audioDataRMS = np.array(rms(audioData, 256, 128)); print('audioDataRMS shape', audioDataRMS.shape)
audioData = np.copy(audioDataRMS)

resolution = 10.0
x = np.arange(0.0, 360.0, (1.0/resolution)); x *= np.pi/180.0; y = np.copy(x)
xAngle = np.cos(x); yAngle = np.sin(y); audioTempBuffer = np.zeros_like(x)

fig, ax = mplt.subplots(1); fig.tight_layout(pad=0); fig.set_facecolor('black')
ax.axis('off'); ax.set_xlim([-2.0, 2.0]); ax.set_ylim([-2.0, 2.0]); ax.set_facecolor('black')

oneSecondInSamples = SAMPLERATE * 60.0; PI = np.pi; TWOPI = 2.0 * PI; K = TWOPI / SAMPLERATE; 
frequency = 5000.0; sawtoothLen = int(oneSecondInSamples/frequency)
sawtooth = generateSawtooth(frequency, 0.25, sawtoothLen); idx = 0

currentSample = 0; percentOverlap = 1.009; overlapSize = int((360*resolution)/percentOverlap); sampleIncrement = (audioTempBuffer.shape[0] - overlapSize)
remainingSamples = audioTempBuffer.shape[0] - overlapSize - 1; numberOfSteps = int( audioData.shape[0]/sampleIncrement )
#print('overlapSize', overlapSize, 'audio Samples minus overlap', remainingSamples, "num time steps", numberOfSteps)

anim = FuncAnimation(fig, func=animFunc, frames=range(numberOfSteps), interval=1)
anim.save("circularAudioVisualizer.gif", fps=30)
#mplt.show()
