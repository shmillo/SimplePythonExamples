import numpy as np
import matplotlib.pyplot as mplt

def amplitude(xv, yv, n, m): 
    return np.abs(np.sin(n*np.pi*xv/2)*np.sin(m*np.pi*yv/2) - np.sin(m*np.pi*xv/2)*np.sin(n*np.pi*yv/2))

x = y = np.linspace(-1, 1, 1000)
xv, yv = np.meshgrid(x, y)

mplt.pcolormesh(xv, yv, amplitude(xv, yv, 1, 7))
mplt.show()