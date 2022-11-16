import sympy as sp
import numpy as np
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as mplt

def g(x, surfaceFunc):
  dx1 = sp.diff(surfaceFunc, x1)
  dx2 = sp.diff(surfaceFunc, x2)
  return np.array([sp.lambdify(x1, dx1)(x[0]), sp.lambdify(x2, dx2)(x[1])])

x = np.array([0.0, 10.0]); 
x1History = []; x1History.append(x[0])
x2History = []; x2History.append(x[1])

x1, x2 = sp.symbols('x1 x2', real=True)
surfaceFunc = 0.5*x1**2.0 - 4.0*x1 + 5.0*x2**2.0 + 30.0*x2

tol = 0.0001
progress = [float(0.5*x[0]**2.0 - 4.0*x[0] + 5.0*x[1]**2.0 + 30.0*x[1])]
for i in range(100):
  if(np.sqrt(float(g(x, surfaceFunc)[0]**2.0) + float(g(x, surfaceFunc)[1]**2.0)) > tol):
    s = -g(x, surfaceFunc)
    a = sp.Symbol('a')
    l = g(x + a*s, surfaceFunc).dot(s)
    a = sp.solve(l, a)
    if(len(a) == 0):
      a = np.array([0, 0])
    x = x + a*s
    progress.append(float(0.5*x[0]**2.0 - 4.0*x[0] + 5.0*x[1]**2.0 + 30.0*x[1]))
    x1History.append(x[0]); x2History.append(x[1])

xAxis = np.arange(-10.0, 10.0, 0.05); yAxis = np.arange(-10.0, 10.0, 0.05); X, Y = np.meshgrid(xAxis, yAxis)
f =  0.5*X**2.0 - 4.0*X + 5.0*Y**2.0 + 30.0*Y

fig = mplt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, f, alpha = 0.4)
ax.plot(x1History, x2History, progress, color = 'r')
mplt.show()