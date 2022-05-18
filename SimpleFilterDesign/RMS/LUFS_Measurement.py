from cmath import exp, log, log10, pi, sin

def meanSquaredAmplitude(x):
    y = 0.0

    for i in range(len(x)):
        y += (x[i]**2.0) 

    return (y / len(x))

def DFIIdiffEQ(x, a, b):

    N = len(x); A = len(a); B = len(b)
    w = [0.0] * A; y = [0.0] * N

    for i in range(N - 1):

        w[0] = a[0] * x[i]
        for j in range(1, A):
            w[0] -= (a[j] * w[j])
        for j in range(B):
            y[i] += (b[j] * w[j])

        for j in range(A - 1, 0, -1):
            w[j] = w[j - 1]

    return y

aOne = [1.0, -1.69065929318241, 0.73248077421585]
bOne = [1.53512485958697, -2.69169618940638, 1.19839281085285]

aTwo = [1.0, -1.99004745483398, 0.99007225036621]
bTwo = [1.0, -2.0, 1.0]

########## ########## ########## ########## ########## ##########
########## ########## ########## ########## ########## ##########

TWOPI = pi * 2.0

sampleRate = 44100.0
dt = 1.0 / sampleRate

numberOfSeconds = 0.5

simulationLengthInSamples = int( numberOfSeconds * sampleRate )

########## ########## ########## ########## ########## ##########
########## ########## ########## ########## ########## ##########

sineSweepData = [0.0] * simulationLengthInSamples

startFrequency = 1.0
endFrequency = 20000.0

T = numberOfSeconds
tempOne = TWOPI * startFrequency * T
tempTwo = TWOPI * endFrequency * T
tempThree = log( tempTwo / tempOne )
tempFour = tempOne / tempThree

time = 0.0
for i in range( 0, simulationLengthInSamples ):
    sineSweepData[ i ] = sin( tempFour * (exp((time / T) * tempThree) - 1.0) )
    time += dt

########## ########## ########## ########## ########## ##########
########## ########## ########## ########## ########## ##########

filteredSweepData = DFIIdiffEQ(sineSweepData, aOne, bOne)
filteredSweepData = DFIIdiffEQ(filteredSweepData, aTwo, bTwo)

########## ########## ########## ########## ########## ##########
########## ########## ########## ########## ########## ##########

LUFS = -0.691 + (10.0 * log10(meanSquaredAmplitude(filteredSweepData))).real
print(LUFS)

