def function(x):
    return x**2 + 1

def discreteAntiDerivative(a, b, numSteps, alpha):

    #distanceTraveled divided by number of steps taken
    deltaX = (b - a) / numSteps

    #LHS == 0, MP == 0.5, RHS == 1
    offset = (alpha * deltaX)

    areaSum = 0.0
    for i in range(numSteps):

        #Width
        currentXValue = (a + (deltaX * i)) + offset

        #Length
        currentYValue = function(currentXValue)

        #Area = Length * Width
        areaSum += currentYValue

    return deltaX * areaSum


a = 0.0
b = 2.0
nSteps = 100

print("Target Answer = 4.67")

testValue = discreteAntiDerivative(a, b, nSteps, 0)
print("LHS Riemann Sum", testValue)

testValue = discreteAntiDerivative(a, b, nSteps, 0.5)
print("MP Riemann Sum", testValue)

testValue = discreteAntiDerivative(a, b, nSteps, 1.0)
print("RHS Riemann Sum", testValue)

