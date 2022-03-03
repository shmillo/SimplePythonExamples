from tracemalloc import start
import matplotlib.pyplot as mplt

def cubicBezier(x, p0, p1, p2, p3):
    return (((1.0 - x)**3) * p0) + ((3.0*(1.0 - x)**2) * x * p1) + ((3.0*(1.0 - x)*(x**2)) * p2) + ((t**3) * p3)


testData = [-1.0, 1.0, -1.0]
interpolatedPoints = []

numSubPoints = 30
localIncrement = 1.0 / numSubPoints 

offset = 0.4
for i in range( 0, len(testData) - 1 ):
    
    startPoint = testData[ i ]
    endPoint = testData[ i + 1 ]

    globalIncrement = ( (endPoint - startPoint) / (3.0 * offset) )

    p0 = startPoint
    p1 = startPoint + globalIncrement
    p2 = startPoint + globalIncrement * 2.0
    p3 = endPoint

    
    t = 0.0
    for j in range( numSubPoints ):

        interpolatedPoints.append(cubicBezier( t, p0, p1, p2, p3 ))
        t += localIncrement

mplt.axes( xlim = [0, len(interpolatedPoints)], ylim = [-2.0, 2.0] )
mplt.plot( interpolatedPoints )
mplt.grid()
mplt.show()