import numpy as np
import matplotlib.pyplot as mplt

#simplified implementation of fast wavelet transform using db4 wavelet
N = 256
sq3 = 1.73205080757
sq3d4 = sq3 * 0.25
sq3m2 = ( (sq3 - 2.0) * 0.25 )
sq3m1 = sq3 - 1
sq3p1 = sq3 + 1
sq3m1d2 = sq3m1 / 1.41421356237
sq3p1d2 = -1.0 * (sq3p1 / 1.41421356237)
sq3m2d4 = (sq3 - 2.0) * 0.25

S = []
s = []; s1 = []; s2 = []
d = []; d1 = []

S = np.random.rand(N)

#approximation vector step one
for i in range( 0, N - 1, 2 ):
    s1.append( S[i] + sq3 * S[i + 1] )

tempOne = []
tempOne.append( sq3m2 * s1[len(s1) - 1] )
for i in range( 1, len(s1) ):
    tempOne.append( sq3m2 * s1[i] )
#detail vector step one  
count = 0
for i in range( 0, N - 1, 2 ):
    d1.append( S[i + 1] - (sq3d4 * s1[count]) - tempOne[count] )
    count += 1
   
tempTwo = []
for i in range( 1, len(d1) ):
    tempTwo.append( d1[i] )
tempTwo.append( d1[0] )
#approximation step two
for i in range( 0, len(s1) ):
    s2.append( s1[i] - tempTwo[i] )
#final step for both approx and detail
for i in range( 0, len(s2) ):
    s.append( sq3m1d2 * s2[i] )
    d.append( sq3p1d2 * d1[i] )
print(len(s))

############### inverse transform ###############

for i in range(len(s)):
    d1[i] = d[i] * sq3m1d2
    s2[i] = s[i] * sq3p1d2

#circshift d1
tempThree = []
for i in range(1, len(d1)):
    tempThree.append(d1[i])
tempThree.append(d1[0])

for i in range(len(s2)):
    s1[i] =  s2[i] + tempThree[i]

tempFour = []
tempFour.append( sq3m2d4 * s1[len(s1) - 1] )
for i in range(1, len(s1)):
    tempFour.append( sq3m2d4 * s1[i] )
    
R = [0.0] * len(S)
count = 0
for i in range(0, len(S) - 1, 2):

    R[i + 1] = d1[count] + (sq3d4 * s1[count]) + tempFour[count]
    R[i] = s1[count] - (sq3 * R[i + 1])

    R[i] *= -1.0
    R[i + 1] *= -1.0

    count += 1

fig, (ax1, ax2, ax3, ax4) = mplt.subplots(4)

ax1.plot(S, label = 'input')
ax1.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

ax2.plot(s, label = 'approximation vector')
ax2.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

ax3.plot(d, label = 'detail vector')
ax3.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

ax4.plot(R, label = 'reconstructed output')
ax4.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

mplt.show()