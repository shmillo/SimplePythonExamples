import numpy as np
import matplotlib.pyplot as mplt
from scipy.io.wavfile import write

class Bubble:
    def __init__(self, initialRadius, sigma):
        self.initialRadius = initialRadius
        self.sigma = sigma

        self.startFreq = startFrequency(self.initialRadius) 
        self.totalDiameter = (0.00000021875 * self.startFreq)**0.5
        self.diameterRadians = (0.003731804657688)**0.5
        self.B0 = np.pi * self.startFreq * (self.totalDiameter + self.diameterRadians)

def timeVaryingFrequency(sFreq, sig, b0, time):
    return sFreq * (1.0 + sig) * b0 * time

def startFrequency(r):
    v = 0.0
    if(r > 0.0): 
        v = 3.0/r
    else:
        v = 500
    return v

def bubbleAmplitudeEnvelope(b0, time):
    return np.exp(-b0 * time)

def startingFrequencyConstraint(l, h):
    return (3.0/l), (3.0/h)

def mapSlope(oL, oH, iL, iH):
    return (oH - oL) / (iH - iL)

def mapToConstraint(x, oL, iL):
    global mSlope
    output = oL + (mSlope * (x - iL))
    return output

loFrequency, hiFrequency = startingFrequencyConstraint(60, 1000)
numBubbles = 50; initialRadii = np.random.random_sample([numBubbles])
mSlope = mapSlope(loFrequency, hiFrequency, 0.0, 1.0); initialRadii = mapToConstraint(initialRadii, loFrequency, 0.0)
print(loFrequency, hiFrequency, initialRadii)

bubbles = []; globalSigma = 0.005
for i in range(numBubbles):
    bubbles.append(Bubble(initialRadii[i], globalSigma))
bubbles.sort(key=lambda x: x.startFreq, reverse=False)

fig, (ax1, ax2) = mplt.subplots(2); 

SAMPLERATE = 44100.0; dt = 1.0/SAMPLERATE; simulationInSeconds = 2.0; xAxis = np.arange(0.0, simulationInSeconds, dt)
amplitudeArr = np.zeros([numBubbles, len(xAxis)]); 
for i in range(numBubbles):
    amplitudeArr[i] = bubbleAmplitudeEnvelope(bubbles[i].B0, xAxis)
    if(numBubbles < 20):
        ax1.plot(xAxis, amplitudeArr[i], label=("amp. envelope " + str(i)))
    else:
        ax1.plot(xAxis, amplitudeArr[i])
ax1.set_xlim([0.0, 0.2]); ax1.legend()

frequencyPathArr = np.zeros([numBubbles, len(xAxis)])
for i in range(numBubbles):
    frequencyPathArr[i] = timeVaryingFrequency(bubbles[i].startFreq, bubbles[i].sigma, bubbles[i].B0, xAxis)
    if(numBubbles < 20):
        ax2.plot(xAxis, frequencyPathArr[i], label=("frequency slope " + str(i)))
    else:
        ax2.plot(xAxis, frequencyPathArr[i])  
ax2.legend()

fig2 = mplt.figure(figsize=(5, 5)); fig2.tight_layout(pad=0); ax3 = fig2.add_subplot(111, projection='3d'); ax3.dist = 6.5

finalBubblesArr = np.zeros([numBubbles, len(xAxis)]); twoPi = np.pi * 2.0; ax3.set_xlim([0.0, 0.2])
twoPixAxis = twoPi * xAxis
for i in range(numBubbles):

    finalBubblesArr[i] = np.sin(frequencyPathArr[i] * twoPixAxis )
    finalBubblesArr[i] = finalBubblesArr[i] * amplitudeArr[i]

    normalNumber = finalBubblesArr[i].max()
    for j in range(len(xAxis)):
        finalBubblesArr[i][j] /= normalNumber

    if(numBubbles <= 20):
        ax3.plot(xAxis, finalBubblesArr[i], zs=i, zdir='y'); ax3.dist = 7; ax3.set_xlim([0.0, 0.2])

fig3, ax4 = mplt.subplots(1,1); ax4.set_xlim([0.0, 15000.0])

bubbleVolumeWeight = np.ones([numBubbles, len(xAxis)])
weights = np.zeros(numBubbles)
for i in range(numBubbles):
    weights[i] = (0.9**(numBubbles - i))
    print((0.9**(numBubbles - i)))
weights /= sum(weights)
print("sumWeights ", sum(weights))

for i in range(numBubbles):
    bubbleVolumeWeight[i] *= weights[numBubbles - i - 1]

audioOut = np.zeros(len(xAxis) * 2); maxDelay = int(len(xAxis) * 0.5)
for i in range(numBubbles):
    delayInSamps = int(np.random.rand() * maxDelay)
    for j in range(delayInSamps, len(xAxis) + delayInSamps):
        nonDelayedIndex = j - delayInSamps
        audioOut[j] += (finalBubblesArr[i][nonDelayedIndex] * bubbleVolumeWeight[i][nonDelayedIndex])

normalNumber = audioOut.max()
for i in range(len(xAxis)):
    audioOut[i] /= normalNumber
ax4.plot(audioOut, label='resultant audio output from weighted mix of bubbles'); ax4.legend()

write("ten_bubbles.wav", int(SAMPLERATE), audioOut.astype(np.float32)); print("writing complete")
mplt.show()