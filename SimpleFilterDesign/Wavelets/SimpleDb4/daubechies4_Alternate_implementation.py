from cmath import pi, sin, sqrt
import matplotlib.pyplot as mplt

length = 32; level = 4

y = [0.0] * length; t = [0.0] * length

sq3 = sqrt(3).real
c1 = 1.0 + sq3; c1 *= 0.25
c2 = 3.0 + sq3; c2 *= 0.25
c3 = 3.0 - sq3; c3 *= 0.25
c4 = 1.0 - sq3; c4 *= 0.25

g = [c1, -c2, c3, -c4]; h = [c1, c2, c3, c4]

fig,(ax1,ax2, ax3) = mplt.subplots(3)
ax2.plot( h, label = 'd4 coefficients' )
ax2.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

x = []; sampleRate = 44100.0; dt = 1.0 / sampleRate; f = sampleRate / length; time = 0.0
for i in range(length):
    x.append(i)
    t[i] = sin(2.0 * pi * f * time).real + (0.25 * sin(2.0 * 5.0 * pi * f * time).real) + (0.25 * sin(2.0 * 0.5 * pi * f * time).real) 
    time += dt

ax1.plot( t, label = 'input signal' )
ax1.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )


for i in range(level):

    print("level", i)
    for j in range(length):
        y[j] = 0.0

    len2 = int(length * 0.5)

    for j in range(len2 - 1):
        for k in range(len(h)):
            print(2*j + k)
            y[j] += t[2*j + k] * h[k]
            y[j + len2] += t[2*j + k] * g[k]

    length = int(length * 0.5)

    for j in range(length):
        t[j] = y[j]

ax3.plot( t, label = 'fwt coefficients' )
ax3.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

mplt.show()