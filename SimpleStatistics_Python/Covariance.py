import importlib
import matplotlib.pyplot as mplt

testDataX = [ 0, 1, 2, 3, 4, 5, 6, 7 ]
length = len(testDataX)
N = length

testDataY = [  0.0, 1.0, 1.1, 0.5, 9.99, -10.0, -1.0, -3.2]

meanX = 0.0
meanY = 0.0

for i in range(length):

    meanX += testDataX[i]
    meanY += testDataY[i]

meanX /= length
meanY /= length

sum = 0.0
for i in range(length):
    sum += ( (testDataX[i] - meanX) * (testDataY[i] - meanY) )

#for a single point /= N - 1, for entire data set /= N
sum /= N

print("covariance =", sum)
