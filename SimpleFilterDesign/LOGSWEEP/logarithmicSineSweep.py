
import importlib

import matplotlib.pyplot as mplt
from cmath import exp, log, log10, pi, sin

TWOPI = pi * 2.0

########## ########## ########## ########## ########## ##########
########## ########## ########## ########## ########## ##########

sampleRate = 44100.0
dt = 1.0 / sampleRate

numberOfSeconds = 0.5

simulationLengthInSamples = int( numberOfSeconds * sampleRate )

########## ########## ########## ########## ########## ##########
########## ########## ########## ########## ########## ##########

sineSweepData = [0.0] * simulationLengthInSamples

startFrequency = 1.0
endFrequency = 100.0

T = numberOfSeconds
tempOne = TWOPI * startFrequency * T
tempTwo = TWOPI * endFrequency * T
tempThree = log( tempTwo / tempOne )
tempFour = tempOne / tempThree

time = 0.0
for i in range( 0, simulationLengthInSamples ):
    sineSweepData[ i ] = sin( tempFour * (exp((time / T) * tempThree) - 1.0) )
    time += dt


########## ########## ########## ########## ########## ##########
########## ########## ########## ########## ########## ##########


mplt.axis([ 0, simulationLengthInSamples, -1.0, 1.0 ])
mplt.plot(sineSweepData)

mplt.show()