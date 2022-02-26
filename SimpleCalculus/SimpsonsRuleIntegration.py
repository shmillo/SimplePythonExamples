def function(x):
    return x**2

def discreteAntiDerivativeSimpsons(a, b, numSteps):

    #distanceTraveled divided by number of steps taken
    deltaX = (b - a) / numSteps

    areaSum = 0.0
    for i in range(numSteps + 1):

        #Width
        currentXValue = (a + (deltaX * i))

        #Length
        currentYValue = function(currentXValue)

        if i > 0 and i < numSteps:
            if i%2 == 1:
                currentYValue *= 4.0
            elif i%2 == 0:
                currentYValue *= 2.0  

        areaSum += currentYValue

    #Area = Length * Width
    return (deltaX * 0.3333) * areaSum

a = 0.0
b = 8.0
numSteps = 100

testValue = discreteAntiDerivativeSimpsons(a, b, numSteps)
print("testValue", testValue)
print("targetValue", 170.67)