from cmath import pi, sin
import matplotlib.pyplot as mplt

def convolveCompress(F, X):

    N = len(F); n = len(X)

    x = [0.0] * (((2*N) - 2) + n); index = 0
    for i in range( N - 1, (N - 1) + n ):
        x[i] = X[index]; index += 1

    I = [ h for h in range(2, (n + N - 1), 2) ]; m = len(I)
    y = [0.0] * m

    if(len(y)%2 == 0):
        for i in range(2, (n + N - 1) - 1, 2):
            for j in range( N - 1 ):
                y[int(i/2)] += F[N - 1 - j] * x[i + j]
    elif(len(y)%2 == 1):
        for i in range(2, (n + N - 1) - 2, 2):
            for j in range( N - 1 ):
                y[int(i/2)] += F[N - 1 - j] * x[i + j]
    
    return y

fig, (ax1, ax2, ax3, ax4) = mplt.subplots(4)

#fake wavelet for testing purposes
l = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15]
#set up test signal, naive additive synthesis
n = 256; F = [0.0] * n; sampleRate = 44100.0; dt = 1.0 / sampleRate; t = 0.0
for i in range(n):
    F[i] = sin(2.0 * pi * 20.0 * t).real + sin(2.0 * pi * 10000.0 * t).real + sin(2.0 * pi * 300.0 * t).real + sin(2.0 * pi * 1000.0 * t).real + sin(2.0 * pi * 6000.0 * t).real 
    t += dt
#plot initial signal
ax1.plot(F)
#downsample and average for the first time
stepOne = convolveCompress(l, F)
ax2.plot( stepOne )
#downsample and average for the second time
stepTwo = convolveCompress(l, stepOne)
ax3.plot( stepTwo )
#downsample and average for the third time
stepThree = convolveCompress(l, stepTwo)
ax4.plot( stepThree )
#display results
mplt.show()