from cmath import exp, pi, sqrt
import cmath
import matplotlib.pyplot as mplt

def normalDistribution(x, mean, sdev):
    return ((1.0/(sdev * sqrt(2.0*pi))) * exp( -0.5 * ((x - mean)/sdev)**2.0 ).real)

def standardNormalDistribution(x, mean, sdev):
    z = (x - mean)/sdev
    return normalDistribution(z, mean, sdev)

def findMean(D):

    N = len(D)

    sum = 0.0
    for i in range( N ):
        sum += D[i]

    return sum / N

def standardDeviation(D, mean):

    N = len(D)
    variance = 0.0
    for i in range( N ):
        variance += (D[i] - mean)**2.0
    variance /= ( N - 1 )

    return sqrt(variance).real
    

N = 19
Data = [0.7172434347, 0.8522019641, 0.1244905158, 0.4848811938, 0.7028144963, 0.9475833956, 0.7354890894, 0.226688442, 0.8404232442, 0.07220278888, 0.2736180989, 0.1149523256, 0.6989576416, 0.7318413349, 0.2736539094, 0.5987106347, 0.4035076739, 0.2711943395, 0.8339335744]
Data.sort()

nDist = [0.0] * N
snDist = [0.0] * N
sanityCheck = [0.0] * N
xAxis = [0.0] * N

average = findMean(Data)
print("mean ", average)
standardDev = standardDeviation(Data, average)
print("standard deviation ", standardDev)

axisInc = (standardDev*6.0) / N
temporary = (standardDev*-3.0)

for i in range( N ):

    xAxis[i] =  temporary
    temporary += axisInc
    print(xAxis[i])

    nDist[i] = normalDistribution( Data[i], average, standardDev )
    snDist[i] = standardNormalDistribution( Data[i], average, standardDev )

fig, ( ax1, ax2 ) = mplt.subplots(2)

ax1.plot(nDist, 's', label = "normal distribution")
ax2.plot(xAxis, snDist, 's', label = "standard normal distribution")

ax1.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )
ax2.legend( bbox_to_anchor = (0.0, 1), loc = 'upper left' )

mplt.show()