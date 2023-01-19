import numpy as np
import matplotlib.pyplot as mplt

def morlet(s_omega):
    global fourierwl

    _omega0 = 5.0
    fourierwl = 4 * np.pi/(_omega0 + np.sqrt(2.0 + _omega0**2))

    H = np.ones(len(s_omega))
    n = len(s_omega)
    H[s_omega < 0.0] = 0.0

    xhat = 0.75112554 * ( np.exp(-(s_omega - _omega0)**2/2.0)) * H
    return xhat

def setscales(ndata, largestscale, notes, scaling):
    global noctave, nscale, scales

    if scaling == "log":
        if notes <= 0: notes=1 
        # adjust nscale so smallest scale is 2 
        noctave = np.log2( ndata/largestscale/2 )
        nscale = notes * noctave
        scales = np.zeros(int(nscale), dtype=float)
        for j in range(int(nscale)):
            scales[j] = ndata/(scale * (2.0**(float(nscale-1-j)/notes)))
        
    elif scaling=="linear":
        nmax = ndata/largestscale/2
        scales = np.arange(float(2), float(nmax))
        nscale = len(scales)

    return


TWOPI = np.pi * 2.0
sampleRate = 44100.0; dt = 1.0 / sampleRate

numberOfSeconds = 0.5; simulationLengthInSamples = int( numberOfSeconds * sampleRate )

########## ########## ########## ########## ########## ##########
########## ########## ########## ########## ########## ##########

sineSweepData = [0.0] * simulationLengthInSamples
startFrequency = 1000.0; endFrequency = 10000.0

T = numberOfSeconds
tempOne = TWOPI * startFrequency * T; tempTwo = TWOPI * endFrequency * T
tempThree = np.log( tempTwo / tempOne ); tempFour = tempOne / tempThree

time = 0.0
for i in range( 0, simulationLengthInSamples ):
    sineSweepData[ i ] = np.sin( tempFour * (np.exp((time / T) * tempThree) - 1.0) )
    time += dt
data = np.array( sineSweepData )


plotpower2d = True
Nlo = 0; Nhi = sampleRate//4

notes = 16
scaling = "log" #"linear" #
largestscale = 10; order = 2

ndata = len(data)
order = order; scale = largestscale
setscales(ndata, largestscale, notes, scaling); print("num scales", nscale)
cwt = np.zeros((int(nscale), ndata), dtype = np.complex64)
omega = np.array((list(range(0, ndata//2)) + list(range(-ndata//2, 0)))) * (2.0*np.pi/ndata)
datahat = np.fft.fft(data)

for scaleindex in range(int(nscale)):
    currentscale = scales[scaleindex]
    s_omega = omega * currentscale
    psihat = morlet(s_omega)
    psihat = psihat * np.sqrt(2.0 * np.pi * currentscale)
    convhat = psihat * datahat
    W = np.fft.ifft(convhat)
    cwt[scaleindex, 0:ndata] = W 

pwr = (cwt * np.conjugate(cwt)).real
scalespec = np.sum(pwr, axis=1)/scales
y = fourierwl * scales
x = np.arange(0, simulationLengthInSamples, 1.0)

fig = mplt.figure(1)

ax = mplt.axes([0.4, 0.1, 0.55, 0.4]); ax.axis('off'); mplt.xlim(0, simulationLengthInSamples)
plotcwt = np.fabs(cwt.real) #pwr
im = mplt.imshow(plotcwt, cmap = mplt.cm.jet, extent=[x[0], x[-1], y[0], y[-1]], aspect='auto')

ax2 = mplt.axes([0.4, 0.54, 0.55, 0.3]) 
mplt.xlim(0, simulationLengthInSamples); 
mplt.plot(data, 'b-')

ax3 = mplt.axes([0.08, 0.1, 0.29, 0.4])
mplt.xlabel('Power'); mplt.ylabel('Period [s]')
vara = 1.0
if scaling=="log":
    mplt.loglog(scalespec/vara+0.01, y,'b-')
else:
    mplt.semilogx(scalespec/vara+0.01, y, 'b-')
mplt.ylim(y[0], y[-1]); mplt.xlim(20000.0, 0.01)
    
mplt.show()