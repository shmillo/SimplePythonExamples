import numpy as np
import matplotlib.pyplot as mplt

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
mplt.plot(signal)
mplt.show()