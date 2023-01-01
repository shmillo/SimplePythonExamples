import numpy as np
import matplotlib.pyplot as mplt

def naiveDFT(x):
    N = np.size(x)
    X = np.zeros((N,), dtype=np.complex128)
    for m in range(0,N):    
        for n in range(0,N): 
            X[m] += x[n] * np.exp(-np.pi*2j*m*n/N)
    return X

def naiveIDFT(x):
    N = np.size(x)
    X = np.zeros((N,), dtype=np.complex128)
    for m in range(0,N):
        for n in range(0,N): 
            X[m] += x[n] * np.exp(np.pi*2j*m*n/N)
    return X/N

def F(x):
    return np.sin( 2.0 * np.pi * 100.0 * x )

sampleRate = 44100; end = 0.1
time = np.linspace(0, end, num=int(sampleRate*end)); print(time.shape)
signal = F(time)

fig, (ax1, ax2, ax3) = mplt.subplots(3)

Xk = naiveDFT(signal); Xk = Xk[:np.size(Xk)//2]
amp = np.sqrt(Xk.real**2.0 + Xk.imag**2.0)/np.size(Xk)
phase = np.arctan2(Xk.imag, Xk.real)

ax1.plot(Xk, label='real half of DFT'); ax1.set_xscale('log'); ax1.legend()
ax2.plot(amp, label='magnitudes'); ax2.set_xscale('log'); ax2.legend()
ax3.plot(phase, label='phase'); ax3.set_xscale('log'); ax3.legend()
mplt.show()