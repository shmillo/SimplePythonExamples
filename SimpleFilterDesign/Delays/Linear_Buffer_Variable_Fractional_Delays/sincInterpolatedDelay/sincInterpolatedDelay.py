import numpy as np
import matplotlib.pyplot as mplt

def linearConvolution(f, h):

  n = f.shape[0] + h.shape[0] - 1
  fftF = np.fft.fft(f, n); fftH = np.fft.fft(h, n)
  frequencyDomainConvolution = fftF * fftH
  return np.fft.ifft(frequencyDomainConvolution).real

def SINC(delay, nTaps):
    sinc = np.zeros(nTaps)
    t = (nTaps - 1)//2
    for i in range(-t, 1, 1):
        t1 = np.pi * (i - delay); t2 = np.pi * (-i - delay)
        v1 = np.sin( t1 ) / t1; v2 = np.sin( t2 ) / t2
        if(i == 0):
            sinc[i] = v1
        else:
            sinc[nTaps+i] = v1; sinc[-i] = v2
    
    return sinc

nTaps = 3000; delay = 1000.5
sFunc = SINC(delay, nTaps)

time = np.linspace(0, 1028, 1028)
signalData = np.sin(2.0 * np.pi * 20.0 * time)

fig, (ax1, ax2) = mplt.subplots(2)
ax1.plot(np.hstack((signalData, np.zeros(sFunc.shape[0]))), label='orginal signal')
ax2.plot(linearConvolution(signalData, sFunc), label='convolved and shifted signal')
mplt.show()