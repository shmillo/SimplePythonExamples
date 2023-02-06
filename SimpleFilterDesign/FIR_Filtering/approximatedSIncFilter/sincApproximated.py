import numpy as np
import matplotlib.pyplot as mplt

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
mplt.plot(SINC(delay, nTaps))
mplt.show()