from ast import BitAnd
import importlib
from cmath import cos, exp, log, log10, pi, sin
import matplotlib.pyplot as mplt

##################### ##################### #####################
##################### ##################### #####################

TWOPI = 2.0 * pi

fs = 44100.0
dt = 1.0 / fs

BW = 0.01

fc = 200.0
bandwidth = 8000.0
fc2 = fc + bandwidth

fc /= fs
wc = TWOPI * fc

fc2 /= fs
wc2 = TWOPI * fc2

max = int( 4.0 / BW )
max += 1

print( "kernelLength = ", max )

middle = int( max * 0.5 )

##################### 

h = [0.0] * max 
w = [0.0] * max
taps = [0.0] * max
x = [0.0] * max

##################### 

sum = 0
i = 0
for n in range(-middle, middle):

    nm = n + middle

    w[i] = 0.42 - (0.5 * cos((TWOPI*i) / max)) + (0.08 * cos(((2.0*TWOPI) * i) / max))

    if n == 0:
         h[nm] = (2.0 * fc2) - (2.0 * fc)
    else:
        h[nm] = (sin(wc2 * n)/(pi * n)) - (sin(wc * n)/(pi * n))
      
    h[nm] *= w[i] 
    i += 1


##################### ##################### #####################
##################### ##################### #####################

numberOfSeconds = 0.15
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

    convolvedOutput[i] = accum
    newest += 1
			
##################### ##################### #####################
##################### ##################### #####################

fig, (ax1, ax2, ax3) = mplt.subplots(3)

ax1.axis([ 0, max, -1.0, 1.0 ])
ax1.plot( h )

ax2.axis([ 0, simulationLength, -1.1, 1.1])
ax2.plot( sineSweepData )

ax3.axis([ 0, simulationLength, -1.1, 1.1])
ax3.plot( convolvedOutput )

mplt.show()