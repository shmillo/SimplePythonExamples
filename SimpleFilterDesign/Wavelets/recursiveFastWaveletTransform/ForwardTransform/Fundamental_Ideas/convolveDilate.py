from cmath import pi, sin
import matplotlib.pyplot as mplt

def convolveDilate(F, X, k):

    N = len(F); n = len(X)
    x = [0.0] * (2 * (n + N - 1))

    index = 0
    for i in range(n):
        x[(N - 1 + (2*i))] = X[index]; index += 1

    m = (2*n) + N - 1; y = [0.0] * m
    for i in range(m):
        for j in range(N):
            y[i] += F[N - j - 1] * x[i + j]

    yNew = [0.0] * k; index = 0
    print( "len(yNew)", len(yNew), " k + N - 1",  k + N - 1, "len(y)", len(y), "len(N)", N )
    for i in range(k): #(N, k + N - 1):
        yNew[i] = y[index]; index += 1
    return yNew

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
stepOne = convolveDilate(l, F, 2*len(F))
ax2.plot(stepOne)
stepTwo = convolveDilate(l, stepOne, 2*len(stepOne))
ax3.plot(stepTwo)
stepThree = convolveDilate(l, stepTwo, 2*len(stepTwo))
ax4.plot(stepThree)
mplt.show()