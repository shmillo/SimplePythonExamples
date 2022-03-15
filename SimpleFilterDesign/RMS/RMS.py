from scipy.io import wavfile
from cmath import sqrt
import numpy as np
import matplotlib.pyplot as mplt

def rms(X, frameLength, hopLength):

    rms = []
    for i in range(0, len(X), hopLength):
        rmsCurrent = np.sqrt( np.sum(X[i:i + frameLength]**2.0) / frameLength )
        rms.append(rmsCurrent)

    return rms


sampleRate, data = wavfile.read('/Users/shawnmilloway/Desktop/EP_Zen/Impo/gtr_all_the_analog.wav')

testArray = rms( data, 1024, 512 )

fig, (ax1, ax2) = mplt.subplots( 2 )

ax1.axis([0, len(data)*0.30, -1.0, 1.0])
ax1.plot( data, label = 'input' )

ax2.axis([0, 2000, -1.0, 1.0])
ax2.plot( testArray, label = 'RMS' )

ax1.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )
ax2.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

mplt.show()