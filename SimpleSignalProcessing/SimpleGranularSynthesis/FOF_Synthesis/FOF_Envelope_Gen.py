import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as mplt

def globalEnvelopeFunction(a, b, x):
    #guassian function
    return (1.0/np.sqrt(2.0*np.pi*b)) * np.exp(-0.5*(1.0/b)*((x-a)**2.0))

fig, (ax1, ax2, ax3, ax4) = mplt.subplots(4)

SAMPLERATE = 44100.0; dt = 1.0/SAMPLERATE

envelopeLengthInSeconds = 0.020; envelopeLengthInSamples = int(envelopeLengthInSeconds*SAMPLERATE); #print(envelopeLengthInSamples)

omega = 2.0 * np.pi * 700.0; formantAmplitude = 1.0

envelope = []; signal = []; t = 0.0
for i in range( envelopeLengthInSamples ):
    envelope.append( formantAmplitude * np.exp(-140.0 * t) )
    signal.append( envelope[i] * np.sin(omega * t) )
    t += dt

formantLength = len(signal); 
ax1.plot(envelope, label='formant amplitude shape'); ax1.legend(fontsize=10)
ax2.plot(signal, label='frequency content'); ax2.legend(fontsize=10)

pitchPeriods = 60
for i in range( pitchPeriods ):
    for j in range( formantLength ):
        signal.append(signal[j])

globalAmplitude = [0.0] * len(signal); #print(len(globalAmplitude), len(signal))
envelopeIncrement = 2.5/len(signal); t = 0.0
for i in range( len(signal) ):
    globalAmplitude[i] = globalEnvelopeFunction(1.195, 0.15, t); t += envelopeIncrement
    signal[i] *= globalAmplitude[i]

ax3.plot(globalAmplitude, label='global envelope'); ax3.legend(fontsize=10)
ax4.plot(signal, label='final output'); ax4.legend(fontsize=10)

signal = np.array(signal)
write("example.wav", int(SAMPLERATE), signal.astype(np.float32)); print("done")
mplt.show()

