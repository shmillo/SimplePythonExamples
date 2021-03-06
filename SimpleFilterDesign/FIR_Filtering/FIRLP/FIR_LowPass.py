import importlib
from cmath import cos, exp, log, log10, pi, sin
import matplotlib.pyplot as mplt

##################### ##################### #####################
##################### ##################### #####################

TWOPI = 2.0 * pi

fs = 44100.0
dt = 1.0 / fs

BW = 0.009

fc = 1000.0
fc /= fs
wc = TWOPI * fc

max = int( 4.0 / BW )
print( "kernelLength = ", max )
hm = int( max * 0.5 )

##################### 

h = [0.0] * max 
w = [0.0] * max
taps = [0.0] * max
x = [0.0] * max

##################### 

sum = 0
for n in range(1, max):

    w[n] = 0.42 - (0.5 * cos((TWOPI*n) / max)) + (0.08 * cos(((2.0*TWOPI) * n) / max))

    if (n - hm) == 0:

         h[n] = 2.0 * fc

    else:

        h[n] = sin(TWOPI * fc * (n - hm)) / (pi * (n - hm))
        h[n] *= w[n] 

    sum += h[n]

for s in range(1, max):
    h[s] /= sum

##################### ##################### #####################
##################### ##################### #####################

numberOfSeconds = 1
simulationLength = int( numberOfSeconds * fs )

sineSweepData = [0.0] * simulationLength

startFrequency = 1.0
endFrequency = 20000.0

T = numberOfSeconds
tempOne = TWOPI * startFrequency * T
tempTwo = TWOPI * endFrequency * T
tempThree = log( tempTwo / tempOne )
tempFour = tempOne / tempThree

time = 0.0
for i in range( 0, simulationLength ):
    sineSweepData[ i ] = sin( tempFour * (exp((time / T) * tempThree) - 1.0) )
    time += dt


##################### ##################### #####################
##################### ##################### #####################

convolvedOutput = [0.0] * simulationLength
temporary = [0.0] * max

xIndex = 0
newest = 0

for i in range( 0, simulationLength ):

    if newest == max:
        newest = 0
        
    temporary[ newest ] = sineSweepData[ i ]
    xIndex = newest

    accum = 0.0
    kernel = 0.0
    for j in range( 0, max ):

        accum += h[ j ] * temporary[ xIndex ]
        kernel += h[ j ]

        xIndex -= 1
        if xIndex == -1:
            xIndex = max - 1

    convolvedOutput[i] = accum / kernel
    newest += 1
			
##################### ##################### #####################
##################### ##################### #####################

fig, (ax1, ax2, ax3) = mplt.subplots(3)

ax1.axis([ 0, max, -0.5, 0.5])
ax1.plot( h )

ax2.axis([ 0, simulationLength, -1.0, 1.0])
ax2.plot( sineSweepData )

ax3.axis([ 0, simulationLength, -1.0, 1.0])
ax3.plot( convolvedOutput )

mplt.show()