#declare X Data points
testDataX = [1, 2, 3, 4, 5, 6, 7]
lengthX = len(testDataX)
n = lengthX

##############  ##############  ##############

#declare Y Data points
testDataY = [1.5, 3.8, 6.7, 9.0, 11.2, 13.6, 16.0]
lengthY = len(testDataY)

##############  ##############  ##############

#find the Variance, or squared error, of Y values

#first take the mean of Y
meanY = 0.0

for i in range(lengthY):
    meanY += testDataY[i]
meanY /= lengthY

#subtract mean from individual Y data points, then take the magnitude
SEy = 0.0

for i in range(lengthY):
     SEy += (testDataY[i] - meanY)**2.0
print("Variance of Y", SEy)

##############  ##############  ##############

sumX = 0.0
sumY = 0.0

sumXY = 0.0
sumXX = 0.0

for i in range(lengthX):

    sumX += testDataX[i]
    sumY += testDataY[i]

    sumXY += testDataX[i] * testDataY[i]
    sumXX += testDataX[i] * testDataX[i]

#slope of a regression line through data points
m = (n * sumXY - (sumX * sumY)) / (n * sumXX - (sumX**2))
print("slope")
print(m)

#intercept of a regression line through data points
b = (sumY - (m * sumX)) / n
print("intercept")
print(b)

##############  ##############  ##############

#plug in X coords into regression line, subtract from actual Y values

sumR = 0.0

residuals = []

for i in range(lengthX):
    guess = (m * testDataX[i] - b)
    residuals.append( testDataY[i] - guess )
    sumR += residuals[i]
print("residuals of individual points", residuals)

SEline = sumR**2.0
print("Squared Error of Regression Line", SEline)

#percentage of variation not described by regression line
percentNot = SEline/SEy

#percentage of variation that IS described by regression line
coefficientOfDetermination = 1.0 - percentNot
print("coeff of Determination", coefficientOfDetermination)

##############  ##############  ##############
