import numpy as np
import matplotlib.pyplot as mplt

def linearConvolution(f, h):

  n = f.shape[0] + h.shape[0] - 1
  fftF = np.fft.fft(f, n); fftH = np.fft.fft(h, n)
  frequencyDomainConvolution = fftF * fftH
  return np.fft.ifft(frequencyDomainConvolution).real

#################### ##################### #####################
##################### ##################### #####################

TWOPI = 2.0 * np.pi

fs = 44100.0; dt = 1.0 / fs

BW = 0.01

fc = 200.0; bandwidth = 8000.0; fc2 = fc + bandwidth

fc /= fs; wc = TWOPI * fc
fc2 /= fs; wc2 = TWOPI * fc2
max = int( 4.0 / BW ); max += 1

print( "kernelLength = ", max )

middle = int( max * 0.5 )

#####################

h = np.zeros(max); w = np.zeros(max); taps = np.zeros(max); x = np.zeros(max)

#####################

sum = 0; i = 0
for n in range(-middle, middle):

    nm = n + middle

    w[i] = 0.42 - (0.5 * np.cos((TWOPI*i) / max)) + (0.08 * np.cos(((2.0*TWOPI) * i) / max))

    if n == 0:
         h[nm] = (2.0 * fc2) - (2.0 * fc)
    else:
        h[nm] = (np.sin(wc2 * n)/(np.pi * n)) - (np.sin(wc * n)/(np.pi * n))

    h[nm] *= w[i]
    i += 1

h /= h.max()

##################### ##################### #####################
##################### ##################### #####################

simulationLength = 4056
sineSweepData = np.zeros(simulationLength)

startFrequency = 1.0; endFrequency = 20000.0

T = (simulationLength/44100.0)
tempOne = TWOPI * startFrequency * T
tempTwo = TWOPI * endFrequency * T
tempThree = np.log( tempTwo / tempOne )
tempFour = tempOne / tempThree

time = 0.0
for i in range( 0, simulationLength ):
    sineSweepData[ i ] = np.sin( tempFour * (np.exp((time / T) *
tempThree) - 1.0) )
    time += dt

convolvedOutput = np.array( linearConvolution(h,sineSweepData) )
convolvedOutput /= convolvedOutput.max()

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