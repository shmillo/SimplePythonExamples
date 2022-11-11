import numpy as np
import matplotlib.pyplot as mplt

def add_arrow(line, position=None, direction='right', size=15, color=None):

    if color is None:
        color = line.get_color()

    xdata = line.get_xdata()
    ydata = line.get_ydata()

    if position is None:
        position = xdata.mean()
    # find closest index
    start_ind = np.argmin(np.absolute(xdata - position))
    if direction == 'right':
        end_ind = start_ind + 1
    else:
        end_ind = start_ind - 1

    line.axes.annotate('',
        xytext=(xdata[start_ind], ydata[start_ind]),
        xy=(xdata[end_ind], ydata[end_ind]),
        arrowprops=dict(arrowstyle="->", color=color),
        size=size
    )

def approximateGradient(f, h, slope, intercept, xAxis):
    dF = []
    for x in xAxis:
        dF.append(((-f(x + (2.0*h), slope, intercept) + (8.0*f(x+h, slope, intercept)) - (8.0*f(x - h, slope, intercept)) + f(x - (2.0*h), slope, intercept))/(12.0*h)) + (((h**4.0)/30.0)*f(x, slope, intercept)))
    return dF

start = -1.0; end = 1.0; step = 0.1
xAxis = np.arange(start, end + step, step)
slope = 1.0; intercept = 0.0

func = lambda x, m, b: m*x**2 + b
trueGradient = lambda x: 2.0*x
lineFunction = lambda x, m, b: m*x + b

Y = [ func(i, slope, intercept) for i in xAxis ]
#trueDy = [ trueGradient(i) for i in xAxis ]
approximatedDy = approximateGradient(func, step, slope, intercept, xAxis)

x = start; arrayCount = 0; lineSegment = 0; index = 0; overlap = 3; numberOfSegments = 10; lineSizeInSteps = 5
lineAxes = [ [0.0]*lineSizeInSteps for _ in range(numberOfSegments) ]
linesArray = [ [0.0]*lineSizeInSteps for _ in range(numberOfSegments) ]
for i in range(numberOfSegments):
    if(i > 0): 
        x -= overlap*step
    temporarySlope = approximatedDy[index]; 
    temporaryIntercept = func(x, slope, intercept); 
    for j in range(lineSizeInSteps):
        lineAxes[i][j] = x
        linesArray[i][j] = lineFunction(x, temporarySlope, 0) - temporaryIntercept
        x += step; 
    index += int( len(xAxis)/numberOfSegments )
    line = mplt.plot(lineAxes[i], linesArray[i])[0]
    add_arrow(line)
 
mplt.plot(xAxis, Y, '-', alpha = 0.5); 
#mplt.plot(xAxis, approximatedDy); mplt.plot(xAxis, trueDy); 
mplt.show()