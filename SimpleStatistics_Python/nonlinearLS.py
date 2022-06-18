from cmath import exp
from numpy import log
import matplotlib.pyplot as mplt

def nonlinearLeastSquares(X, Y):

    sumX = 0.0; sumT = 0.0; sumZ = 0.0; sumTZ = 0.0
    sumTT = 0.0; n = len(X)
    for i in range(n):
        z = log(Y[i]); sumZ += z
        x = X[i]; sumX += x
        t = x; sumT += t; sumTZ += t * z; sumTT += t*t
    aOne = ((n * sumTZ) - (sumT * sumZ)) / ((n*sumTT) - (sumT**2.0))
    aZero = (sumZ/n) - (aOne * (sumT/n))
    return aOne, exp(aZero).real

numTestArray_2022 = [1,1,1,2,1,1,1,1,2,1,2,1,1,1,2,2,2,3,6,3,2,2,4,8,3,7,4,5,11,8,6,7,5,6,14,12,11,18,8,13,11,17,17,11,19,15,17,16,27,27,20,28,34,29,23,24,23,28,33,21,16,26,29,21,31,20,12,23,18,22,22,16,15,13,13,19,22,25,24,30,23,33]
numTestArrayGrid = [i for i in range(len(numTestArray_2022))]

slope, intercept = nonlinearLeastSquares(numTestArrayGrid, numTestArray_2022)
print(slope, intercept)

leastSquaresCurve = []
for i in range(len(numTestArray_2022)):
    leastSquaresCurve.append(intercept*exp(slope*i))
mplt.plot(leastSquaresCurve); mplt.plot(numTestArray_2022, '.')
mplt.show()