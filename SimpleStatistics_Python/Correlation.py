testDataX = [ 1, 2, 3, 4, 5, 6 ]
lengthX = len(testDataX)
n = lengthX

testDataY = [ 2, 4, 7, 9, 12, 14 ]

sumX = 0.0
sumY = 0.0
sumXY = 0.0

sumXX = 0.0
sumYY = 0.0

for i in range(lengthX):

    sumX += testDataX[i]
    sumXX += testDataX[i]**2

    sumY += testDataY[i]
    sumYY += testDataY[i]**2

    sumXY += (testDataX[i] * testDataY[i])

dnom = ( n * sumXX - sumX**2 ) * ( n * sumYY - sumY**2 )
num = ( n * sumXY - (sumX * sumY) )
correlation =  num / (dnom**0.5)

print("correlation")
print(correlation)    