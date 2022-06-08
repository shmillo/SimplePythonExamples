from cmath import pi, sin
import matplotlib.pyplot as mplt

steps = 8
lod = [ 0.33267054, 0.8068915, 0.4598775, -0.13501102, -0.08544128, 0.035226293 ]; hid = [0.0] * len(lod); L = len(lod);  
for i in range( L - 1, 0, -1 ):
    if( i%2 == 0 ): hid[ i ] = lod[ (L-1) - i ]; 
    else: hid[ i ] = -1.0 * lod[ (L-1) - i ]

sampleRate = 44100.0; dt = 1.0/sampleRate; t = 0.0
inputSignal = [0.0] * 256; sMatrix = [[0.0] * len(inputSignal) for _ in range(steps)]
for i in range(len(inputSignal)):
    inputSignal[i] = ( sin(2.0 * pi * 100.0 * t) + sin(2.0 * pi * 200.0 * t) + sin(2.0 * pi * 2000.0 * t) )
    t += dt    
    sMatrix[0][i] = inputSignal[i]
wMatrix = [[0.0] * len(inputSignal) for _ in range(steps)]

approxCoeffs = []; detailCoeffs = []
for j in range( 1, steps ):
    #print("step = ", j)
    for n in range( 0, int(len(inputSignal)/(2**j)) ):
        #print("n = ", n)
        for k in range( max(1, 2*n - len(lod) + 1), 2*n):
            #print("k = ", k, " 2.0*n - k = ", 2*n - k)
            old = sMatrix[j - 1][k]
            sMatrix[j][n] += old * lod[2*n - k]
            wMatrix[j][n] += old * hid[2*n - k]
        approxCoeffs.append(sMatrix[j][n])
        detailCoeffs.append(wMatrix[j][n])
        
fig, (ax1, ax2, ax3) = mplt.subplots(3)
ax1.plot(inputSignal, label = 'input')  
ax1.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )
ax2.plot( approxCoeffs, label = 'approxCoeff' )
ax2.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )
ax3.plot( detailCoeffs, label = 'detailCoeff' )
ax3.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )
mplt.show()