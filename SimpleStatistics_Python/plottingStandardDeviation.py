from cProfile import label
from cmath import sqrt
import matplotlib.pyplot as mplt

testData = [0.0, 1.0, 2.0, 4.0, 2.0, 1.0, -1.0]
length = len(testData)

localVariance = []

mean = 0.0
for i in range(length):
    mean = mean + testData[i]
mean /= length
meanArray = [ mean ] * length

totalVariance = 0.0
for i in range(length):

    #first half of variance for a single point
    localVariance.append( ( testData[ i ] - mean )**2 )

    #sum for total
    totalVariance += localVariance[ i ]

    #standard deviation of a single point
    # with bessel's correction : (length - 1)
    localVariance[i] = sqrt( localVariance[i]  / ( length - 1 ) ).real

totalVariance /= length

standardDeviation = sqrt(totalVariance).real
standardDeviationUpper = mean + standardDeviation
standardDeviationLower = mean - standardDeviation 


mplt.plot( testData, 's', label = 'samples' )

mplt.vlines(x = (length * 0.5), ymin = [standardDeviationLower], ymax = [standardDeviationUpper], label = 'standard deviation', colors = 'green' )

mplt.plot( meanArray, label = 'mean' )

mplt.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

mplt.show( )