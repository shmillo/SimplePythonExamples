import matplotlib.pyplot as mplt

def quadraticBezierCurve(x, minValue, midValue, maxValue):

    return midValue + ((1.0 - x)*(1.0 - x))*(minValue - midValue) + (x*x)*(maxValue - midValue)

dataSet = [ -100.0, -50.0, 1.0, -10.0, 20.0 ]
deviation = [ 0.1, 0.9, 0.1, 0.1, 0.9 ]

numSubPoints = 10
localPointIncrement = 1.0 / numSubPoints

interpolatedData = [0.0] * (len(dataSet) * numSubPoints + 1)

currentIndex = 0
for i in range( len(dataSet) ):

    if i < len(dataSet) - 1 :
        startPoint = dataSet[i]
        print("sPoint =", startPoint)

        endPoint = dataSet[i + 1]
        print("ePoint =", endPoint)

        midPoint = ( startPoint + ((endPoint - startPoint) * deviation[i]) )
        print("mPoint =", midPoint)

    elif i >= len(dataSet) - 1:

        startPoint = interpolatedData[ currentIndex - 1 ]
        print("sPoint =", startPoint)

        endPoint = dataSet[i]
        print("ePoint =", endPoint)

        midPoint = ( startPoint + ((endPoint - startPoint) * deviation[i]) )
        print("mPoint =", midPoint)


    if i == len(dataSet):
        numIterations = numSubPoints + 1

    else:
        numIterations = numSubPoints

    t = 0.0
    for j in range(numIterations):

        interpolatedData[ currentIndex ] =  quadraticBezierCurve( t, startPoint, midPoint, endPoint )
        
        t += localPointIncrement
        currentIndex += 1

print(currentIndex)
fig, ax = mplt.subplots()
mplt.plot( interpolatedData )
ax.set( xlim = (0, 40), ylim = (-100, 20) )
ax.grid()
mplt.show()