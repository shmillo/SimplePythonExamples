import numpy as np
import matplotlib.pyplot as mplt

def DFT2D(data):
    F = np.zeros(data.shape, dtype=np.complex64)
    n, m = data.shape[:2]

    for u in np.arange(n):
        for v in np.arange(m):

            for x in np.arange(n):
                for y in np.arange(m):

                    F[u,v] += data[x,y] * np.exp( (-1j*2.0*np.pi) * (((u*x)/n) + ((v*y)/m)) )

    return F/np.sqrt(n*m)

def IDFT2D(fftData):
    F = np.zeros(fftData.shape, dtype=np.complex64)
    n, m = fftData.shape[:2]

    for u in np.arange(n):
        for v in np.arange(m):

            for x in np.arange(n):
                for y in np.arange(m):

                    F[u,v] += fftData[x,y] * np.exp( (1j*2.0*np.pi) * (((u*x)/n) + ((v*y)/m)) )

    return F/np.sqrt(n*m)
    
fig, (ax1, ax2, ax3) = mplt.subplots(3); 

n = 16; m = 16
signalData = np.random.rand(n, m)
ax1.set_aspect('equal')
ax1.contourf(signalData)

twoDDFT = DFT2D(signalData)
ax2.set_aspect('equal')
ax2.contourf(twoDDFT)

reconstructedData = IDFT2D(twoDDFT)
ax3.set_aspect('equal')
ax3.contourf(reconstructedData)

mplt.show()