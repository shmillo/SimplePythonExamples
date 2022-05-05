from cmath import pi
from math import sin
import matplotlib.pyplot as mplt

def HaarTransform(x):

    N = len(x)
    n = int(N * 0.5)

    X = [ [0.0] * 2 for _ in range(n) ]

    index = 0
    for i in range(n):
        for k in range( 2 ):

            X[i][k] = x[index]
            index += 1

    s = [0.0] * n
    d = [0.0] * n
    SD = [0.0] * N

    index = 0
    for i in range(n):
        for k in range( 2 ):

            s[i] += 0.5 * X[i][k]

            if(k == 0):
                d[i] += -0.5 * X[i][k]
            elif(k == 1):
                d[i] += 0.5 * X[i][k]

        SD[index] = s[i]
        SD[n + index] = d[i]
        index += 1

    return SD
    
def InverseHaar(x):

    N = len(x)
    n = int(N * 0.5)
    Y = [ [0.0] * 2 for _ in range(n) ]
    R = [0.0] * N

    index = 0
    for i in range( n ):
        for k in range( 2 ):

            if(k == 0):
                Y[i][k] = x[index]
            if(k == 1):
                Y[i][k] = x[index + n]

        index += 1
    
    a = [0.0] * n
    b = [0.0] * n

    index = 0
    for i in range( n ):
        for k in range( 2 ):

            b[i] += Y[i][k]

            if(k == 0):
                a[i] +=  Y[i][k]
            elif(k == 1):
                a[i] -=  Y[i][k]

        R[index] = a[i]
        index += 1
        R[index] = b[i]
        index += 1

    return R

###### ###### ###### ###### ###### ###### 
###### ###### ###### ###### ###### ###### 

sampleRate = 44100.0
dt = 1.0 / sampleRate

numSeconds = 0.1
simulationLengthInSamples = int( 256 )


###### ###### ###### ###### ###### ###### 
###### ###### ###### ###### ###### ###### 

f = 300
sineData = [0.0] * simulationLengthInSamples
time = 0.0
for i in range(simulationLengthInSamples):
    sineData[i] = sin(2.0 * pi * f * time).real + sin(2.0 * pi * 2.0 * f * time).real
    time += dt

###### ###### ###### ###### ###### ###### 
###### ###### ###### ###### ###### ###### 

haarArr = HaarTransform(sineData)
reconstructedData = InverseHaar( haarArr )

###### ###### ###### ###### ###### ###### 
###### ###### ###### ###### ###### ###### 

fig, ( ax1, ax2, ax3 ) = mplt.subplots(3)

ax1.plot( sineData, label = 'Input Signal' )
ax1.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

ax2.plot( haarArr, label = 'Haar Coefficients' )
ax2.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

ax3.plot( reconstructedData, label = 'Reconstructed Data' )
ax3.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

mplt.show()