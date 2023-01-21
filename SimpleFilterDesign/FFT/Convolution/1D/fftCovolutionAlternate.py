import numpy as np
import matplotlib.pyplot as mplt

def nearestPow2(v):
  print(v)
  v -= 1
  v |= v >> 1
  v |= v >> 2
  v |= v >> 4
  v |= v >> 8
  v |= v >> 16
  v += 1
  print(v)
  return v
 
def FFT(P):

    n = len(P)

    if n == 1:
        return P

    else:
        w = np.exp((2.0 * np.pi * 1.0j) / n)


        Pe = []; Po = []
        for i in range(0, n, 2):
            Pe.append(P[ i ])
        for i in range(1, n, 2):
            Po.append(P[ i ])

        ye = FFT(Pe); yo = FFT(Po)

        y = np.zeros(n, dtype=complex)
        for q in range(int(n * 0.5)):
            y[q] = ye[q] + (w**q)*yo[q]
            y[q + int(n/2)] = ye[q] - (w**q)*yo[q]

    return y

def iFFT(P):

    n = len(P)

    if n == 1:
        return P

    else:
        w = np.exp((-2.0 * np.pi * 1.0j) / n)


        Pe = []; Po = []
        for i in range(0, n, 2):
            Pe.append(P[ i ])
        for i in range(1, n, 2):
            Po.append(P[ i ])

        ye = iFFT(Pe); yo = iFFT(Po)

        y = np.zeros(n, dtype=complex)
        for q in range(int(n * 0.5)):
            y[q] = ye[q] + (w**q)*yo[q]
            y[q + int(n/2)] = ye[q] - (w**q)*yo[q]

    return y
   
def linearConvolution(f, h):
 
  n = f.shape[0] + h.shape[0] - 1
  nP2 = nearestPow2(int(n))
  print(h.shape, f.shape, n, nP2)
 
  h = np.array(np.hstack((h, np.zeros(nP2 - h.shape[0]))))
  f = np.array(np.hstack((f, np.zeros(nP2 - f.shape[0]))))
  print(h.shape, f.shape)
 
  fftF = FFT(f); print(fftF.size); fftH = FFT(h); print('ffth', fftH.size)
  frequencyDomainConvolution = fftF * np.conj(fftH)
  print(frequencyDomainConvolution )
  print('convolutionSize', frequencyDomainConvolution.size)
 
  return np.real( iFFT(frequencyDomainConvolution) )[:f.shape[0]]

#################### ##################### #####################
##################### ##################### #####################

TWOPI = 2.0 * np.pi

fs = 44100.0; dt = 1.0 / fs

BW = 0.01

fc = 200.0; bandwidth = 500.0; fc2 = fc + bandwidth

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

#h /= h.max()

##################### ##################### #####################
##################### ##################### #####################

numberOfSeconds = 0.15
simulationLength = int( numberOfSeconds * fs )

sineSweepData = np.zeros(simulationLength)

startFrequency = 1.0; endFrequency = 20000.0

T = numberOfSeconds
tempOne = TWOPI * startFrequency * T
tempTwo = TWOPI * endFrequency * T
tempThree = np.log( tempTwo / tempOne )
tempFour = tempOne / tempThree

time = 0.0
for i in range( 0, simulationLength ):
    sineSweepData[ i ] = np.sin( tempFour * (np.exp((time / T) * tempThree) - 1.0) )
    time += dt

convolvedOutput = linearConvolution(h, sineSweepData)
reversedIndexing = np.linspace(convolvedOutput.shape[0]-1, 0, num=convolvedOutput.shape[0], dtype=np.int16)
convolvedOutput = convolvedOutput[reversedIndexing]
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