import numpy as np
import matplotlib.pyplot as mplt

def functionOne(a, b, x):
    return (a * x)/(b + x)

def gaussian(a, b, x):
    return (1.0/np.sqrt(2.0*np.pi*b)) * np.exp(-0.5*(1.0/b)*((x-a)**2.0))

def Jacobian(f, a, b, x):
    eps = 1e-6
    gradA = (f(a + eps, b, x) - f(a - eps, b, x))/(2.0 * eps)
    gradB = (f(a, b + eps, x) - f(a, b  - eps, x))/(2.0 * eps)
    return np.column_stack([gradA, gradB])

def Gauss_Newton(f, x, y, a0, b0, tol, max_iter):
    old = new = np.array([a0, b0])
    for itr in range(max_iter):
        old = new
        J = Jacobian(f, old[0], old[1], x)
        dy = y - f(old[0], old[1], x)
        new = old + np.linalg.inv(J.T@J)@J.T@dy
        if(np.linalg.norm(old - new) < tol):
            break
    return new

x = np.linspace(0, 5, 50) 
y = functionOne(2, 3, x) + np.random.normal(0, 0.1, size = 50)
mplt.scatter(x,y) 
a, b = Gauss_Newton(functionOne, x, y, 5, 1, 1e-5, 10)
mplt.plot(x, functionOne(a,b,x))
mplt.show()