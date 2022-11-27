import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

def rotator(X, Y, R):
    
    rotOne = np.cos(R); rotTwo = np.sin(R)
    tempXOne = rotOne * X; tempXTwo = rotTwo * X
    tempYOne = rotOne * Y; tempYTwo = rotTwo * Y

    tempOne = tempYOne - tempXTwo; tempTwo = tempXOne + tempYTwo

    return tempOne, tempTwo

def animation_func(i):
    global xRotate, yRotate, zRotate, X, Y, Z

    ax.cla(); ax.axis('off')
    yRotate  = (yRotate + 0.01)%180

    stepOneX, stepOneY = rotator(X, Y, zRotate)
    stepTwoX, finalY = rotator(stepOneY, Z, yRotate)
    finalX, finalZ = rotator(stepOneX, stepTwoX, xRotate)

    ax.scatter(finalX, finalY, finalZ, '.')

fig = mplt.figure(); fig.tight_layout(pad=0); ax = fig.add_subplot(111, projection='3d');  ax.axis('off')
 
xAxis = np.arange(0, 2, 0.5); yAxis = np.arange(0, 2, 0.5); zAxis = np.arange(0, 2, 0.5); X, Y, Z = np.meshgrid(xAxis, yAxis, zAxis); 

zRotate = -10; yRotate = -10; xRotate = 10

anim = FuncAnimation(fig, func=animation_func, frames=np.linspace(0, 500, num=500), interval=10)
anim.save('rotating_Cube_3D.gif')
mplt.show()