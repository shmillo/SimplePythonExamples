import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

xAxis = np.arange(0, 8, 1); yAxis = np.arange(0, 8, 1); X, Y = np.meshgrid(xAxis, yAxis)

twoPi = np.pi * 2.0
f = 2.0; fs = 1.0/44100.0
sizeArray = np.zeros([8, 8])

t = 0.0; timer = 0
for i in range(10000):
    
    t += 100.0 * fs
    
    temp = t; signal = []
    for i in range(8):
        signal.append(np.sin(twoPi * f * temp))
        temp += np.pi/7.0

    mplt.plot(signal, '.')
    mplt.draw()
    mplt.pause(fs)
    mplt.cla()
