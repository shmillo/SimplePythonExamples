import numpy as np
import matplotlib.pyplot as mplt

def functionOne(a, b, x):
    return (a * x)/(b + x)

def gaussian(a, b, x):
    print(a, b)
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

def l2norm(X):
    xTemp = []
    sumSquared = 0.0
    for i in range(len(X)):
        xTemp.append(X[i])
        sumSquared += X[i]*X[i]
    sumSquared = 1.0/(sumSquared**0.5)
    for i in range(len(X)):
        xTemp[i] *= sumSquared
    return xTemp

def normalize(X):
    xTemp = []; maximum = max(X)
    for i in range(len(X)):
        xTemp.append(X[i]/maximum)
    return xTemp

x = np.linspace(0, 5, 50)
y = gaussian(1.195, 0.15, x) + np.random.normal(0, 0.01, size = 50)
mplt.scatter(x,y) 

a, b = Gauss_Newton(gaussian, x, y, 2, 1, 1e-5, 4)
testCurve = gaussian(a,b,x); 
mplt.plot(x, testCurve)
mplt.show()