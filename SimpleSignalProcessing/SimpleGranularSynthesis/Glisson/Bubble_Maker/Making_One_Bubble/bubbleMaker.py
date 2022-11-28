import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as mplt

def timeVaryingFrequency(sigma, time):
    global startFreq, B0
    return startFreq * (1.0 + sigma) * B0 * time

def startFrequency(r):
    v = 0.0
    if(r > 0.0): 
        v = 3.0/r
    else:
        v = 500
    return v

def bubbleAmplitudeEnvelope(time):
    global B0
    return np.exp(-B0 * time)

fig, (ax1, ax2, ax3) = mplt.subplots(3)

SAMPLERATE = 44100.0; dt = 1.0/SAMPLERATE
simulationLengthSeconds = 2; simulationLengthSamples = simulationLengthSeconds * SAMPLERATE
xAxis = np.arange(0.0, simulationLengthSeconds, dt)

sigma = 0.03 #increasing sigma slows upwards direction of the frequency shift and slows the envelope decay
initialRadius = 0.02 #smaller radius means higher start frequency and shorter amplitude envelope 
startFreq = startFrequency(initialRadius) #conversion from radius to starting freq point, doesn't yield exact hz value

totalDiameter = (0.00000021875 * startFreq)**0.5
diameterRadians = (0.003731804657688)**0.5
B0 = np.pi * startFreq * (totalDiameter + diameterRadians)

amplitudeEnvelope = (sigma * initialRadius) * bubbleAmplitudeEnvelope(xAxis)
ax1.plot(amplitudeEnvelope, label='amplitude shape of a single bubble'); ax1.legend()

twoPI = np.pi * 2.0
frequencyComponent = np.sin(twoPI * timeVaryingFrequency(sigma, xAxis) * xAxis)
ax2.set_xlim([0,8000]); ax2.plot(frequencyComponent, label='frequency content of a single bubble'); ax2.legend()

finalOutput = frequencyComponent * amplitudeEnvelope
normalizeNumber = finalOutput.max() #output will be too quiet without normalization
for i in range(len(finalOutput)):
    finalOutput[i] /= normalizeNumber
ax3.set_xlim([0,10000]); ax3.plot(finalOutput, label='final output, a solitary bubble'); ax3.legend()

#write("single_bubble.wav", int(SAMPLERATE), finalOutput.astype(np.float32)); print("done")
mplt.show()