import numpy as np
import matplotlib.pyplot as mplt

fig, ax = mplt.subplots(figsize = (6, 6))

SAMPLERATE = 44100.0; dt = 1.0/SAMPLERATE
numSamps = 2**12; print("numSamps ", numSamps)
frameTimeline = np.array(list(range(numSamps)))

sf = 22000; stheta = 0; numberOfVoices = 3; numberOfNoteChangeEvents = 10
timelineSignal = np.array([dt*i for i in range(0, numSamps)])

frequencyModifier = np.random.rand(numberOfVoices, numberOfNoteChangeEvents); 
magnitudeModifier = np.random.rand(numberOfVoices, numberOfNoteChangeEvents)

noteChangeTimes = np.array(numSamps * np.random.rand(numberOfVoices, numberOfNoteChangeEvents - 1), dtype=np.int64)
noteChangeTimes = np.array(np.append(noteChangeTimes, np.zeros([numberOfVoices, 1], dtype=np.int64), axis=1), dtype=np.int64)
noteChangeTimes.sort()
#print("samples at which notes will change", noteChangeTimes)
durations = np.array(noteChangeTimes[:, 1:] - noteChangeTimes[:, :-1])
#print(durations.shape)
#print("durations [in samples]", durations)
envelopes = np.zeros([numberOfVoices, numberOfNoteChangeEvents, np.max(durations)])
#print(envelopes.shape)
for voice in range(numberOfVoices):
    for note in range(numberOfNoteChangeEvents - 1):
        envelopeLength = durations[voice, note]
        envelopeLengthD2 = envelopeLength//2
        for i in range(envelopeLength):
            envelopes[voice, note, i] = (envelopeLengthD2 - abs(envelopeLengthD2 - abs(envelopeLengthD2 - (envelopeLengthD2 + i))))/envelopeLengthD2
#mplt.plot(envelopes[0, 2])
#print(envelopes.shape)

envelopeMaster = np.ones([numberOfVoices, timelineSignal.shape[0]])
#print(envelopeMaster.shape, envelopes.shape, noteChangeTimes.shape)
for voice in range(numberOfVoices):
    for note in range(numberOfNoteChangeEvents - 1): 
        envelopeLength = durations[voice, note]
        for timeStep in range(envelopeLength):
            envelopeMaster[voice, timeStep+noteChangeTimes[voice, note]] = envelopes[voice, note, timeStep]
#mplt.plot(envelopeMaster[0])
#print(envelopes[0])

signal = np.zeros([numberOfVoices, numSamps])
for voice in range(numberOfVoices):
    for note in range(numberOfNoteChangeEvents - 1):
        beginPoint = noteChangeTimes[voice, note]; endPoint = noteChangeTimes[voice, note+1]
        signal [voice, beginPoint:endPoint] += magnitudeModifier[voice, note] * np.sin(2.0 * np.pi * (sf*frequencyModifier[voice, note]) * timelineSignal[beginPoint:endPoint])
    mplt.plot(signal[voice] * envelopeMaster[voice])

mplt.show()