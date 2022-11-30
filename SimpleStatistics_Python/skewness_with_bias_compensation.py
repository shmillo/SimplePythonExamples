import numpy as np
from math import floor

def vectorizedVariance(testData):
    return sum((testData - vectorizedMean(testData))**2.0) / testData.shape[0]

def standardDeviation(testData):
    return vectorizedVariance(testData)**0.5

def vectorizedMean(testData):
    return sum(testData) / testData.shape[0]

def skewness(testData):
    n = testData.shape[0]
    G1 = ((n*(n - 1))**0.5) / (n - 2)
    skewness = (sum((testData - vectorizedMean(testData))**3.0)/n) / (sum((testData - vectorizedMean(testData))**2.0)**1.5/n)
    return G1 * skewness

def standardError(testData):
    n = testData.shape[0]
    return (((6.0*n) * (n - 1)) / ((n - 2.0)*(n + 1)*(n + 3)))**0.5

def mode(arr):
    if arr==[]:
        return None
    else:
        return max(set(arr), key=arr.count)

def median(testData):
    n = testData.shape[0]
    return (testData[int(floor(n * 0.5))] + testData[int(floor(n * 0.5 + 0.5))]) * 0.5

def pearsonSkew(testData):
    meanValu = vectorizedMean(testData)
    medianValu = median(testData)
    modeValu = mode(testData)
    standardDeviationValu = standardDeviation(testData)

    SkOne = (meanValu - modeValu)/standardDeviationValu
    SkTwo = (3.0*(meanValu - modeValu))/standardDeviationValu

    return SkOne, SkTwo
    
sunObservations = [101.00, 82.00, 66.00, 35.00, 31.00, 7.00, 20.00, 92.00, 154.00, 125.00, 85.00, 68.00, 
38.00, 23.00, 10.00, 24.00, 83.00, 132.00, 131.00, 118.00, 90.00, 67.00, 60.00, 47.00, 
41.00, 21.00, 16.00, 6.00, 4.00, 7.00, 14.00, 34.00, 45.00, 43.00, 48.00, 42.00, 28.00, 
10.00, 8.00, 2.00, 0.00, 1.00, 5.00, 12.00, 14.00, 35.00, 46.00, 41.00, 30.00, 24.00, 
16.00, 7.00, 4.00, 2.00, 8.00, 17.00, 36.00, 50.00, 62.00, 67.00, 71.00, 48.00, 28.00, 
8.00, 13.00, 57.00, 122.00, 138.00, 103.00, 86.00, 63.00, 37.00, 24.00, 11.00, 15.00, 
40.00, 62.00, 98.00, 124.00, 96.00, 66.00, 64.00, 54.00, 39.00, 21.00, 7.00, 4.00, 23.00,
55.00, 94.00, 96.00, 77.00, 59.00, 44.00, 47.00, 30.00, 16.00, 7.00, 37.00, 74.00]
sunObservations = np.array(sunObservations)

print( skewness(sunObservations)/standardError(sunObservations) )


