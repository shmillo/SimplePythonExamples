from cmath import exp, pi, sin, sqrt
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

#must be a power of 2
size = 256
testData = []

SAMPLERATE = 44100.0
dt = 1.0/SAMPLERATE

f = 1.0/(size/SAMPLERATE)
time = 0.0
for i in range(size):

    value = sin(2.0 * pi * 2.0 * f * time).real + (1.5 * sin(2.0 * pi * 8.0 * f * time).real) +  (0.9 * sin(2.0 * pi * 22.50 * f * time).real)
    value += 0.13 * sin(2.0 * pi * 28.0 * f * time).real + (0.5 * sin(2.0 * pi * 9.1230 * f * time).real) +  (0.9 * sin(2.0 * pi * 42.50 * f * time).real)
    value += 0.23 * sin(2.0 * pi * 18.0 * f * time).real + (0.5 * sin(2.0 * pi * 12.1230 * f * time).real) +  (0.9 * sin(2.0 * pi * 32.50 * f * time).real)
    
    testData.append( value )

    time += dt

fftData = FFT(testData)

##### DO SOMETHING WITH FFT DATA #####

binFrequencies = []
magnitudes = []

for u in range( int(0.5 * len(fftData)) - 1 ):

    binFrequencies.append( (u * SAMPLERATE) / size  )
    magnitudes.append( sqrt( fftData[u].real**2 + fftData[u].imag**2 ).real )


max_value = max( magnitudes )
max_index = magnitudes.index(max_value)
peakFrequency = (max_index * SAMPLERATE) / size
print("predicted frequency = ", peakFrequency )

##### DO SOMETHING WITH FFT DATA #####

ifftData = iFFT(fftData)

for q in range( len(ifftData ) ):
    ifftData[q] /= size


fig, (ax1, ax2, ax3) = mplt.subplots(3)

ax1.plot( testData, label = 'original' )
ax2.plot( ifftData, label = 'reconstructed' )
ax3.plot( binFrequencies, magnitudes, label = 'FFT' )
ax3.set_xscale('log')

ax1.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )
ax2.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )
ax3.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

mplt.show()