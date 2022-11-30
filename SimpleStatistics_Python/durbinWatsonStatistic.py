import numpy as np
import matplotlib.pyplot as mplt

def vectorizedMean(testData):
    return sum(testData) / testData.shape[0]

def vectorizedVariance(testData):
    return sum((testData - vectorizedMean(testData))**2.0)

def vecorizedLeastSquares(testDataX, testDataY):

    n = testDataX.shape[0]
    squaredErrorY = vectorizedVariance(testDataY)
    sumX = sum(testDataX); sumY = sum(testDataY)
    
    slopeOfRegressionLine = (n * sum(testDataX * testDataY) - (sumX * sumY)) / (n * sum(testDataX**2.0) - (sumX**2.0))
    interceptOfRegressionLine = (sumY - (slopeOfRegressionLine * sumX)) / n

    residuals = testDataY - ((slopeOfRegressionLine * testDataX) - interceptOfRegressionLine)
    sumOfSquaredError = sum(residuals)**2.0

    coefficientOfDetermination = sumOfSquaredError / squaredErrorY
    print(slopeOfRegressionLine, interceptOfRegressionLine, coefficientOfDetermination)

    return slopeOfRegressionLine, interceptOfRegressionLine, residuals

def durbinWatsonStatistic(testDataX, testDataY):
    slope, intercept, eArray = vecorizedLeastSquares(testDataX, testDataY)
    return sum((eArray[1:] - eArray[0:(eArray.shape[0]-1)] )**2.0) /  sum(eArray**2.0)

xAxis = np.linspace(0, 100, num=100)
yAxis = (10.0 * xAxis) + (50.0 * np.random.rand(xAxis.shape[0]))
print(durbinWatsonStatistic(xAxis, yAxis))

slope, intercept, eArray = vecorizedLeastSquares(xAxis, yAxis)
lineEQ = lambda x: (slope * x) + intercept
mplt.plot(xAxis, lineEQ(xAxis)); mplt.plot(yAxis, '.', alpha = 0.5); mplt.show()