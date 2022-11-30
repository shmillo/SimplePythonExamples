import numpy as np
import matplotlib.pyplot as mplt

def calculateLagrangeCoeffs(d):
    h0 = (d * (1.0 + d)) * 0.5
    h1 = (1.0 + d) * (1.0 - d)
    h2 = (-d * (1.0 - d)) * 0.5
    return h0, h1, h2

def maximum(value, comparison):
    outVal = 0.0
    if(value <= comparison):
        outVal = comparison
    elif(value > comparison):
        outVal = value
    return outVal

def calcCurrentDelay():
    global SAMPLERATE, tC, readBuffer, delayTarget, delayCurrent, increment
    
    delayCurrent = delayCurrent + (tC * (delayTarget - delayCurrent))
    increment = writeBuffer.shape[0] / (SAMPLERATE * maximum(delayCurrent, 0.001))

SAMPLERATE = 44100.0; dt = 1.0/SAMPLERATE; tC = 4.0/SAMPLERATE; t = 0.0; lengthOfSimulationInSamples = int( 4 * SAMPLERATE ) 
delayTarget = 0.05; delayCurrent = 0.0; increment = 0.0; phase = 0.0; lastPhase = 0.0
currentWrite = np.zeros(3); readBuffer = np.zeros(lengthOfSimulationInSamples); writeBuffer = np.zeros(lengthOfSimulationInSamples); inputData = np.zeros(lengthOfSimulationInSamples)

for i in range(lengthOfSimulationInSamples):

    inputData[i] = np.sin(2.0 * np.pi * 100.0 * t); t += dt

    calcCurrentDelay()

    fph = int(phase); lastPhase = fph; lInt = phase - fph
    d = lInt
    if(d > 1.0):
        d = 1.0
    elif(d < 0.0):
        d = 0.0
    h0, h1, h2 = calculateLagrangeCoeffs(d)

    indOne = int((fph + 1)%writeBuffer.shape[0]); indTwo = int((fph + 2)%writeBuffer.shape[0]); indThree = int((fph + 3)%writeBuffer.shape[0])
    readBuffer[i] = (h0 * writeBuffer[indOne]) + (h1 * writeBuffer[indTwo]) + (h2 * writeBuffer[indThree])

    phase = phase + increment
    lInc = 1.0/(int(phase) - (lastPhase + 1))
    if(lInc > 1.0):
        lInc = 1.0
    lInt = 0

    currentWrite[0] = inputData[i]
    for track in np.arange(lastPhase, phase, 1.0):

        h0, h1, h2 = calculateLagrangeCoeffs(lInt)

        currentWriteValue = (h0 * currentWrite[0]) + ((h1 * currentWrite[0]) + currentWrite[1])  + ((h2 * currentWrite[0]) + currentWrite[2])
        currentWriteIndex = int(track%writeBuffer.shape[0])
        writeBuffer[currentWriteIndex] = currentWriteValue
        lInt = lInt + lInc
    currentWrite[2] = currentWrite[1]; currentWrite[1] = currentWrite[0]

    if(phase >= writeBuffer.shape[0]):
        phase = phase - writeBuffer.shape[0]

fig, (ax1, ax2) = mplt.subplots(2)
    
ax1.plot(inputData)
ax2.plot(writeBuffer)
mplt.show()
