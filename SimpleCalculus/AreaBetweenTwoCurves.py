Fx = lambda x: 8.0 - 2*x
Gx = lambda x: x*0

def discreteAntiDerivative(function, a, b, numSteps, alpha):

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
b = 4.0
nSteps = 10

#in this example F(x) = 8.0 - 2*x
areaUnderFofX = discreteAntiDerivative(Fx, a, b, nSteps, 0.5)

#in this example G(x) is the x-axis, or G(x) = 0.0 
areaUnderGofX = discreteAntiDerivative(Gx, a, b, nSteps, 0.5)

print("target answer = 16")

area = areaUnderFofX - areaUnderGofX
print("estimated area under the curves = ", area)