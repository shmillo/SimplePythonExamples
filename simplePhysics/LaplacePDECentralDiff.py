
from re import M
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as mplt

height = 10
length = 10

gridSpacing = 1.0

heightInSamples = int( gridSpacing * height )
middle = int(heightInSamples * 0.5)

lengthInSamples = int( gridSpacing * length )

h = 1.0 / ( heightInSamples + 1 )
k = 1.0 / ( lengthInSamples + 1 )

#arr = [[0]*cols]*rows
values = [[0.0]*lengthInSamples for _ in range(heightInSamples)]
error = [[0.0]*lengthInSamples for _ in range(heightInSamples)]

maxError = 1.0
tolerance = 1e-10

boundaryValue = 3.0
values[middle][middle] = boundaryValue

for i in range(lengthInSamples):
    values[0][i] = boundaryValue
    values[i][0] = boundaryValue
    
numberIterations = 100
for x in range(0, numberIterations):
 
    if abs( maxError ) >= tolerance:

        for i in range( 1, int(heightInSamples - 1) ):
            for j in range( 1, int(lengthInSamples - 1) ):
               
                temporary = 0.25 * ( values[i + 1][j] + values[i - 1][j] + values[i][j + 1] + values[i][j - 1] )
                
                if temporary != 0.0:
                    error[i][j] = abs( (temporary - values[i][j])  / temporary )
                else:
                    error[i][j] = abs( temporary - values[i][j] )

                values[i][j] = temporary

    values[middle][middle] = boundaryValue

    error.sort()
    maxError = error[middle][middle]
    #print(maxError)
    

Xs = range( 0, heightInSamples )
Ys = range( 0, lengthInSamples )
Zs = values

fig = mplt.figure()
ax = fig.gca(projection = '3d')
ax.contour(Xs, Ys, Zs)

mplt.show()

