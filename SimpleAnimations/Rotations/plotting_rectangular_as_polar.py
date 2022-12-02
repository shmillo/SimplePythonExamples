import matplotlib.pyplot as mplt
import numpy as np


twoPi = 2.0*np.pi; numberOfRevolutions = 1.0
upperBound = numberOfRevolutions * twoPi; lowerBound = -upperBound; step = twoPi / 16.0
xAxis = np.arange(lowerBound, upperBound+step, step); yAxis = np.arange(lowerBound, upperBound+step, step); X, Y = np.meshgrid(xAxis, yAxis)

radiusArr = np.arange(X.shape[0]); thetaArr = np.zeros(X.shape[0])
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        thetaArr[j] = np.arctan(X[i][j]/Y[i][j]) if X[i][j] != 0.0 else 0.0
        radiusArr[j] = (X[i][j]**2.0 + Y[i][j]**2.0)**0.5
    thetaCos = np.cos(thetaArr[i]); thetaSin = np.sin(thetaArr[i])

    mplt.plot((thetaCos*X[i] - thetaSin*Y[i]), (thetaCos*X[i] + thetaSin*Y[i]), '.', color='k')

mplt.show()