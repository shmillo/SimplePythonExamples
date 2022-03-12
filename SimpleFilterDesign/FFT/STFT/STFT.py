from cmath import cos, exp, log, pi, sin, sqrt
import matplotlib.pyplot as mplt

def FFT(P):

    n = len(P)

    if n == 1:
        return P

    else:
        w = exp((2.0 * pi * 1.0j) / n)


        Pe = []
        Po = []
        for i in range(0, n, 2):
            Pe.append(P[ i ])
        for i in range(1, n, 2):
            Po.append(P[ i ])

        ye = FFT(Pe)
        yo = FFT(Po)

        y = [0.0] * n
        for q in range(int(n * 0.5)):
            y[q] = ye[q] + (w**q)*yo[q]
            y[q + int(n/2)] = ye[q] - (w**q)*yo[q]

    return y

def iFFT(P):

    n = len(P)

    if n == 1:
        return P

    else:
        w = exp((-2.0 * pi * 1.0j) / n)


        Pe = []
        Po = []
        for i in range(0, n, 2):
            Pe.append(P[ i ])
        for i in range(1, n, 2):
            Po.append(P[ i ])

        ye = iFFT(Pe)
        yo = iFFT(Po)

        y = [0.0] * n
        for q in range(int(n * 0.5)):
            y[q] = ye[q] + (w**q)*yo[q]
            y[q + int(n/2)] = ye[q] - (w**q)*yo[q]

    return y

########## ########## ########## ########## ########## ##########
########## ########## ########## ########## ########## ##########

TWOPI = pi * 2.0

sampleRate = 44100.0
dt = 1.0/sampleRate

numberOfSeconds = 0.5

simulationLengthInSamples = int( numberOfSeconds * sampleRate )

########## ########## ########## ########## ########## ##########
########## ########## ########## ########## ########## ##########

sineSweepData = [0.0] * simulationLengthInSamples

startFrequency = 1.0
endFrequency = 6000.0

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

windowSize = 4096
numWindows = int( simulationLengthInSamples / windowSize ) + 1
print("nWindows ", numWindows)
size = windowSize
windowData = [0.0] * windowSize

for i in range( 0, windowSize ):
    windowData[i] = 0.5 * (1.0 - cos((TWOPI * i)/(windowSize - 1)))

########## ########## ########## ########## ########## ##########
########## ########## ########## ########## ########## ##########

segmentedData = [ [0.0] * windowSize for _ in range(numWindows) ]
fftData = [ [0.0] * windowSize for _ in range(numWindows) ]

for q in range( numWindows ):
    for i in range( 0, windowSize ):

        index = i + (q * windowSize)

        if(index < simulationLengthInSamples):
            segmentedData[q][i] = sineSweepData[ index ]
        else:
            segmentedData[q][i] = 0.0

    fftData[q] = FFT( segmentedData[q] )
 
##### DO SOMETHING WITH FFT DATA #####

binFrequencies = [ [0.0] * windowSize for _ in range(numWindows) ]
magnitudes = [ [0.0] * windowSize for _ in range(numWindows) ]
maxValue = [0.0] * numWindows

for j in range( numWindows ):
    for u in range( int( 0.5 * windowSize ) - 1 ):
        binFrequencies[j][u] = ( (u * sampleRate) / size  )
        magnitudes[j][u] = ( sqrt( fftData[j][u].real**2 + fftData[j][u].imag**2 ).real )

for j in range( numWindows ):
    maxValue[j] = max( magnitudes[j] )
    for u in range( int( 0.5 * windowSize ) - 1 ):
        if(maxValue[j] != 0.0):
            magnitudes[j][u] = magnitudes[j][u] / maxValue[j]

##### ##### ##### ##### ##### ##### #####

reconstructedData = [0.0] * simulationLengthInSamples
ifftData = [ [0.0] * windowSize for _ in range(numWindows) ]

for t in range( numWindows ):
    ifftData[t] = iFFT(fftData[t])
    for k in range( windowSize ):
        index = k + (t * windowSize) 
        if( index < simulationLengthInSamples ):
            reconstructedData[ index ] = ifftData[t][k] / windowSize


########## ########## ########## ########## ########## ##########
########## ########## ########## ########## ########## ##########

fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8) = mplt.subplots( 8 )

ax1.axis([ 0, simulationLengthInSamples, -1.0, 1.0 ])
ax1.plot(sineSweepData, label = 'input')
ax1.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

ax2.axis([ 0, windowSize, -1.0, 1.0 ])
ax2.plot(windowData, label = 'Hann Window')
ax2.legend( bbox_to_anchor = (0.0, 0), loc = 'lower left' )

ax3.plot(segmentedData[2], label = 'First STFT Windowed Input')
ax3.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

ax4.plot(segmentedData[4], label = 'Second STFT Windowed Input')
ax4.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

ax5.plot(magnitudes[0], label = 'First Normalized STFT Frame')
ax5.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )
ax5.set_xscale('log')

ax6.plot(magnitudes[1], label = 'Second Normalized STFT Frame')
ax6.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )
ax6.set_xscale('log')

ax7.plot(magnitudes[2], label = 'Third Normalized STFT Frame')
ax7.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )
ax7.set_xscale('log')

ax8.plot( magnitudes[3], label = 'Fourth Normalized STFT Frame')
ax8.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )
ax8.set_xscale('log')

mplt.show()

mplt.figure(2)
mplt.axis([ 0, simulationLengthInSamples, -1.0, 1.0 ])
mplt.plot(reconstructedData)

mplt.show()
