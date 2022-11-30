import numpy as np
import matplotlib.pyplot as mplt

def correlationVectorized(testDataX, testDataY):
    n = testDataX.shape[0]; sumX = sum(testDataX); sumY = sum(testDataY)
    tempOne = n * sum(testDataX**2.0) - sumX**2.0
    tempTwo = n * sum(testDataY**2.0) - sumY**2.0
    denominator = tempOne * tempTwo
    numerator = n * sum(testDataX * testDataY) - (sumX * sumY)
    return (numerator / (denominator**0.5))

sunObservations = [101.00, 82.00, 66.00, 35.00, 31.00, 7.00, 20.00, 92.00, 154.00, 125.00, 85.00, 68.00, 
38.00, 23.00, 10.00, 24.00, 83.00, 132.00, 131.00, 118.00, 90.00, 67.00, 60.00, 47.00, 
41.00, 21.00, 16.00, 6.00, 4.00, 7.00, 14.00, 34.00, 45.00, 43.00, 48.00, 42.00, 28.00, 
10.00, 8.00, 2.00, 0.00, 1.00, 5.00, 12.00, 14.00, 35.00, 46.00, 41.00, 30.00, 24.00, 
16.00, 7.00, 4.00, 2.00, 8.00, 17.00, 36.00, 50.00, 62.00, 67.00, 71.00, 48.00, 28.00, 
8.00, 13.00, 57.00, 122.00, 138.00, 103.00, 86.00, 63.00, 37.00, 24.00, 11.00, 15.00, 
40.00, 62.00, 98.00, 124.00, 96.00, 66.00, 64.00, 54.00, 39.00, 21.00, 7.00, 4.00, 23.00,
55.00, 94.00, 96.00, 77.00, 59.00, 44.00, 47.00, 30.00, 16.00, 7.00, 37.00, 74.00]
sunObservations = np.array(sunObservations)

autoCorrelationCoeffs = np.zeros(sunObservations.shape[0])
for i in range(25):
    indices = range(i, i + (sunObservations.shape[0]))
    lagArray = sunObservations.take(indices, mode='wrap')
    autoCorrelationCoeffs[i] = correlationVectorized(sunObservations, lagArray)
 
fig, ax = mplt.subplots(1); ax.plot(autoCorrelationCoeffs, label='autocorrelation coeffs'); ax.set_xlim([0, 20]); ax.legend()
mplt.show()