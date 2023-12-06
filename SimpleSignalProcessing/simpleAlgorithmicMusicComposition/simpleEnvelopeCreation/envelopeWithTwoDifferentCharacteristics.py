import numpy as np
import matplotlib.pyplot as mplt

fig, ax = mplt.subplots(figsize = (6, 6))

SAMPLERATE = 44100.0; dt = 1.0/SAMPLERATE
numSamps = 2**12; print("numSamps ", numSamps)
frameTimeline = np.array(list(range(numSamps)))

numberOfNoteChangeEvents = 10
timelineSignal = np.array([dt*i for i in range(0, numSamps)])

noteChangeTimes = np.array(numSamps * np.random.rand(numberOfNoteChangeEvents - 1), dtype=np.int64)
noteChangeTimes = np.array(np.append(noteChangeTimes, np.zeros(1, dtype=np.int64), axis=0), dtype=np.int64)
noteChangeTimes.sort()

durations = np.array(noteChangeTimes[1:] - noteChangeTimes[:-1])
envelope = np.zeros([numberOfNoteChangeEvents, np.max(durations)])
halfEnvelope = envelope[0].shape[0]//2

for note in range(numberOfNoteChangeEvents - 1):
    envelopeLength = durations[note]
    envelopeLengthD2 = envelopeLength//2
    for i in range(envelopeLength):
        envelope[note, i] = (envelopeLengthD2 - abs(envelopeLengthD2 - abs(envelopeLengthD2 - (envelopeLengthD2 + i))))/envelopeLengthD2
    envelope[note, :envelopeLengthD2] = np.exp(-10.0*(1.0 - envelope[note, :envelopeLengthD2]))
    envelope[note, envelopeLengthD2:] = np.log10(1.0 + (9.0 * envelope[note, envelopeLengthD2:]))
    envelope[note] /= envelope[note].max() 
    mplt.plot(envelope[note])
mplt.show()