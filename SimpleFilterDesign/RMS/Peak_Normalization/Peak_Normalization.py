from cmath import sqrt
from scipy.io import wavfile
import matplotlib.pyplot as mplt

sampleRate, data = wavfile.read('/Users/shawnmilloway/Desktop/EP_Zen/Impo/gtr_all_the_analog.wav')

N = len(data)

print(data[100])

maxLeft = 0.0; maxRight = 0.0
for i in range( N - 1 ):
    if( abs(data[i][0]) > maxLeft ):
        maxLeft = data[i][0]
    if( abs(data[i][1] > maxRight) ):
        maxRight = data[i][1]
print(maxLeft)

peakNormScalarLeft = 1.0 / abs(maxLeft)
peakNormScalarRight = 1.0 / abs(maxRight)

normalizedOutput = [ [0.0] * 2 for _ in range(N) ]
print(len(normalizedOutput))

for i in range( N - 1 ):
    normalizedOutput[i][0] = data[i][0] * peakNormScalarLeft
    normalizedOutput[i][1] = data[i][1] * peakNormScalarRight

fig,(ax1,ax2) = mplt.subplots(2)

ax1.plot(data, label = 'input data')
ax1.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

ax2.plot(normalizedOutput, label = 'normalized output data')
ax2.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

mplt.show()