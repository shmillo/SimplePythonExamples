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

def fftShift(fftData):
    
    height, width = fftData.shape
    halfWidth = width//2; halfHeight = height//2

    shifted = np.zeros_like(fftData)

    shifted[(height - halfHeight):height, (width - halfWidth):width] = fftData[:halfHeight, :halfWidth]
    shifted[(height - halfHeight):height, 0:(width - halfWidth)] = fftData[:halfHeight, halfWidth:width]
    shifted[0:(height - halfHeight), (width - halfWidth):width] = fftData[halfHeight:height, :halfWidth]
    shifted[0:(height - halfHeight), 0:(width - halfWidth)] = fftData[halfHeight:height, halfWidth:width]

    return shifted

fig, (ax1, ax2, ax3) = mplt.subplots(3); 

n = 16; m = 16
signalData = np.random.rand(n, m)
ax1.set_aspect('equal')
ax1.contourf(signalData)

twoDDFT = fftShift(DFT2D(signalData))
ax2.set_aspect('equal')
ax2.contourf(twoDDFT)

reconstructedData = IDFT2D(fftShift(twoDDFT))
ax3.set_aspect('equal')
ax3.contourf(reconstructedData)

mplt.show()