import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as mplt

def waveformFunction(x, t):
    return (np.sin(x*t))**2.0

fig, (ax1, ax2, ax3, ax4) = mplt.subplots(4)

SAMPLERATE = 44100.0; dt = 1.0/SAMPLERATE; numSeconds = 1.0; numSamples = numSeconds * SAMPLERATE
fundamentalFrequencyHz = 500.0; periodInSeconds = 2.0 * np.pi * fundamentalFrequencyHz; 
periodInSamples = int(SAMPLERATE / fundamentalFrequencyHz); numPeriods = 5; totalLengthOfPulseInSamps = int(periodInSamples * 0.5) * numPeriods

silenceInSamples = 880; silenceArray = np.zeros(silenceInSamples)

pulseBeginning = 0.0; pulseEnding = totalLengthOfPulseInSamps * dt; pitchedComponent = np.arange(pulseBeginning, pulseEnding, dt); 

startingAmplitude = 1.0; amplitudeDecayFactor = 0.8; 
amplitudeEnvelope = []; temporaryAmplitude = startingAmplitude
for i in range(numPeriods):
    for j in range(int(periodInSamples * 0.5)):
        amplitudeEnvelope.append(temporaryAmplitude)
    temporaryAmplitude *= amplitudeDecayFactor
amplitudeEnvelope = np.append(amplitudeEnvelope, silenceArray)
ax1.plot(amplitudeEnvelope, label='Amplitude Envelope'); ax1.legend()

xAxis = np.arange(0.0, numSeconds, dt); 
waveformArray = waveformFunction(periodInSeconds, pitchedComponent); waveformArray = np.append(waveformArray, silenceArray)
ax2.plot(waveformArray, label='waveform array'); ax2.legend()
print('waveform array', np.shape(waveformArray), 'ampltidue envelope', np.shape(amplitudeEnvelope))
waveformArray = waveformArray * amplitudeEnvelope
ax3.plot(waveformArray, label='waveform array scaled by amplitude envelope with the silence window added'); ax3.legend()

totalRuntimeInSeconds = 30.0; totalRuntimeInSamples = int(totalRuntimeInSeconds * SAMPLERATE)
totalFormantIterations = int(totalRuntimeInSamples / len(waveformArray))
totalOutputArray = []; totalOutputArray = np.append(totalOutputArray, waveformArray)
for i in range(totalFormantIterations):
    totalOutputArray = np.append(totalOutputArray, waveformArray)
ax4.plot(totalOutputArray, label='sample of completed output'); ax4.set_xlim([0, 8000]); ax4.legend()

write("example.wav", int(SAMPLERATE), totalOutputArray.astype(np.float32)); print("done")
mplt.show()
