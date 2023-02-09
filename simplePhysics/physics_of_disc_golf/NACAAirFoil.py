import numpy as np 
import matplotlib.pyplot as plt 

t = 0.1 #maximum thickness as a fraction of the chord
c = 1 #chord length
xc = np.linspace(0, 1.544795, 1000)

#CALCULATION
y1 = (5*t*c)*((0.2969*np.sqrt(xc/c))-(0.3516*(xc/c)**2)+(0.2843*(xc/c)**3) - (0.1015*(xc/c)**4))
y2 = -y1

plt.plot(y1); plt.plot(y2)
plt.show()


