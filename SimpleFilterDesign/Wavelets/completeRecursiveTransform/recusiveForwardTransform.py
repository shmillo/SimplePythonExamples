from cmath import pi, sin, sqrt
import matplotlib.pyplot as mplt
from math import ceil, floor

def convolveCompress(F, X):

    N = len(F); N1 = N - 1; n = len(X)

    x = [0.0] * N1; 
    for i in range(0, n):
        x.append(X[i]); 
    for i in range(N1):
        x.append(0.0)

    if(n%2 == 0):
        I = [ h for h in range(2, (n + N1), 2) ]; 
    if(n%2 == 1):
        I = [ h for h in range(2, (n + N1) + 2, 2) ]; 
    m = len(I); y = [0.0] * (m); 

    for i in range(0, m, 1):
        for j in range(0, N, 1):
            y[i] = y[i] + F[N - 1 - j] * x[I[i] + j - 1]
    return y

def convolveDilate(F, X, k):

    N = len(F); N1 = N - 1; n = len(X)
    x = [0.0] * (2 * (n + N1))

    index = 0
    for i in range(n):
        x[(N1 + (2*i))] = X[index]; index += 1

    m = (2*n) + N1; y = [0.0] * m
    for j in range(1, N + 1):
        for i in range(m):
            y[i] += F[N - j] * x[i + j - 1]

    yNew = [0.0] * k; index = 0
    for i in range(N1 - 1, k + N1 - 1):
        yNew[index] = y[i]; index += 1

    return yNew

def rev(l):
    reversed = [0.0] * len(l)
    index = -1
    for i in range(len(l)):
        reversed[i] = l[index]
        index -= 1
    return reversed

def l2h(l):

    N = len(l); lR = rev(l)

    h = [0.0] * N
    for i in range(len(lR)):
        h[i] = lR[i]

    for i in range(1, N, 2):
        h[i] = -1.0 * h[i]
    hR = rev(h)

    return [h, lR, hR, N]

def wtdl(n, N, alt, Jdes):

    J = 0; m = 0
    if(alt == "tmf" or alt == "cmf"):

        N *= 0.5
        if(N%2 == 1):
            N -= 2
        else:
            N -= 1

        if( N < 2 ):
            N = 2

        while(J < Jdes and n >= N):
                J += 1
                n = int( ceil(n * 0.5) )
                m += n

    elif(alt == "emf" or alt == "evf"):
        while( n >= N and J < Jdes ):
            J += 1
            n = floor((n + N - 1) * 0.5)
            m += n

    m += n
    return [J, m]

def FWT(a, l, alt, Jdes):
    n = len(a)
    [h, lR, hR, N] = l2h(l)
    [J, m] = wtdl(n, N, alt, Jdes); 
    b = [0.0] * (J + 1); b[0] = n; x = []
    x = [0.0] * m

    p = 0
    for j in range(0, J):
 
        d = convolveCompress(h, a); b[j + 1] = len(d)
        
        q = p + b[j + 1] - 1; index = 0
        for y in range(p, q):
            x[y] = (d[index]); index += 1
        p = q + 1

        a = convolveCompress(l, a)

    q = int(p + b[J] - 1); index = 0
    for y in range(p, q):
        x[y] = a[index]; index += 1
    return x, b, J, m
    
def IWT(X, b, l, alt):

    print("b", b)
    N = len(l); h, lR, hR, N = l2h(l); 
    J = (len(b) - 1); q = len(X); p = q - int(b[J]); 

    s = [0.0] * (q - p); index = 0
    for i in range(p, q):
        s[index] = (X[i]); index += 1

    for j in range(J - 1, -1, -1):

        q = p - 1; p = q - int(b[j + 1]) + 1
        d = [0.0] * (q - p); index = 0
        for i in range(p, q):
            d[index] = X[i]; index += 1

        aTemp = convolveDilate(lR, s, b[j]); dTemp = convolveDilate(hR, d, b[j])
        s = [0.0] * len(aTemp)
        for i in range(len(aTemp)):
            s[i] = aTemp[i] + dTemp[i]

    return s

fig, (ax1, ax2, ax3) = mplt.subplots(3)

#DB6 Wavelet
#l = [ 0.33267054, 0.8068915, 0.4598775, -0.13501102, -0.08544128, 0.035226293 ]

#DB12 Wavelet
l = [ 0.021784700327, 0.004936612372, -.166863215412, -.068323121587, 0.694457972958, 1.113892783926, 0.477904371333, -.102724969862, -.029783751299, 0.063250562660, 0.002499922093, -.011031867509 ]
for i in range(len(l)):
    l[i] /= sqrt(2.0)

#transform parameters
n = 256; alt = "evf"; Jdes = 256

#signal parameters and creation, naive additive synthesis
a = [0.0] * n; sampleRate = 44100.0; dt = 1.0/sampleRate; t = 0.0
for i in range(n):
    a[i] = sin(2.0 * pi * 100.0 * t).real + sin(2.0 * pi * 1000.0 * t).real + sin(2.0 * pi * 3000.0 * t).real 
    t += dt
ax3.plot(a)

#run the forward transform
Q, b, J, m = FWT(a, l, alt, Jdes); ax1.plot(Q)
#run the reconstruction
signal = IWT(Q, b, l, alt); ax2.plot(signal)

mplt.show()