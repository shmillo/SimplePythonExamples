import numpy as np
import scipy as sp
from scipy import interpolate
import scipy.sparse.linalg as splinalg
import matplotlib.pyplot as mplt

def forcingFunction(time, point):
    timeDecay = np.maximum( 10.0 - 0.5*time, 0.0, )
    forcedValue = (timeDecay * np.where( ((point[0] > 0.4) & (point[0] < 0.6) & (point[1] > 0.1) & (point[1] < 0.6)), np.array([0.0, 0.3]), np.array([0.0, 0.0]), ))
    return forcedValue

def partialDerivativeX(field):
    global elementLength
    diff = np.zeros_like(field)
    diff[1:-1, 1:-1] = ( (field[2:, 1:-1] - field[0:-2, 1:-1])/(2.0*elementLength) )
    return diff

def partialDerivativeY(field):
    global elementLength
    diff = np.zeros_like(field)
    diff[1:-1, 1:-1] = (field[1:-1, 2:] - field[1:-1, 0:-2]) / (2.0 * elementLength)
    return diff

def laplace(field):
    global elementLength
    diff = np.zeros_like(field)
    diff[1:-1, 1:-1] = (field[0:-2, 1:-1] + field[1:-1, 0:-2] - 4.0*field[1:-1, 1:-1] + field[2:, 1:-1] + field[1:-1, 2:]) / (elementLength**2.0)
    return diff

def divergence(vectorField):
    divergenceApplied = (partialDerivativeX(vectorField[..., 0]) + partialDerivativeY(vectorField[..., 1]))
    return divergenceApplied

def gradientField(field):
    gradientApplied = np.concatenate( (partialDerivativeX(field)[..., np.newaxis], partialDerivativeY(field)[..., np.newaxis], ), axis=- 1)
    return gradientApplied

def curl2D(vectorField):
    curlApplied = partialDerivativeX(vectorField[..., 1]) - partialDerivativeY(vectorField[..., 0])
    return curlApplied

def advect(field, vectorField):
    global xAxis, yAxis, domainSize, coordinates, timeStepLength
    backtracedPositions = np.clip( (coordinates - timeStepLength*vectorField), 0.0, domainSize )
    advectedField = interpolate.interpn( points=(xAxis, yAxis), values=field, xi=backtracedPositions )
    return advectedField

def diffusionOperator(vectorFieldFlattened):
    global timeStepLength, vectorShape, kinematicViscosity
    vectorField = vectorFieldFlattened.reshape(vectorShape)
    diffusionApplied = (vectorField - kinematicViscosity * timeStepLength * laplace(vectorField))
    return diffusionApplied.flatten()

def poissonOperator(fieldFlattened):
    global scalarShape
    field = fieldFlattened.reshape(scalarShape)
    poissonApplied = laplace(field)
    return poissonApplied

domainSize = 1.0
nPoints = 41
nTimeSteps = 20000
timeStepLength = 0.1
kinematicViscosity = 0.00001

elementLength = domainSize / (nPoints - 1)
scalarShape = (nPoints, nPoints); scalarDOF = int(nPoints**2)
vectorShape = (nPoints, nPoints, 2); vectorDOF = int(nPoints**2 * 2)

maxIterCG = None

xAxis = np.linspace(0.0, domainSize, nPoints); yAxis = np.linspace(0.0, domainSize, nPoints); X, Y = np.meshgrid(xAxis, yAxis, indexing="ij")

coordinates = np.concatenate( (X[..., np.newaxis], Y[..., np.newaxis],), axis = -1 )
forcingFunctionVectorized = np.vectorize( pyfunc=forcingFunction, signature="(), (d)->(d)", )

velocitiesPrev = np.zeros(vectorShape)
timeCurrent = 0.0

mplt.figure(figsize=(5,5))

for i in range(nTimeSteps):
    timeCurrent += timeStepLength
    forces = forcingFunctionVectorized(timeCurrent, coordinates, )
    velocitiesForcesApplied = velocitiesPrev + timeStepLength * forces

    velocitiesAdvected = advect(field=velocitiesForcesApplied, vectorField=velocitiesForcesApplied, )
    velocitiesDiffused = splinalg.cg(A=splinalg.LinearOperator(shape=(vectorDOF, vectorDOF), matvec=diffusionOperator, ), b=velocitiesAdvected.flatten(), maxiter=maxIterCG,)[0].reshape(vectorShape)
    pressure = splinalg.cg(A=splinalg.LinearOperator(shape=(scalarDOF,scalarDOF), matvec=poissonOperator, ), b=divergence(velocitiesDiffused).flatten(), maxiter=maxIterCG,)[0].reshape(scalarShape)

    velocitiesProjected = velocitiesDiffused - gradientField(pressure)
    velocitiesPrev = velocitiesProjected

    curl = curl2D(velocitiesProjected)

    mplt.contourf(X, Y, curl, cmap='winter_r', levels=100)
    mplt.quiver(X, Y, velocitiesProjected[..., 0], velocitiesProjected[..., 1])
    mplt.draw()
    mplt.pause(0.0001)
    mplt.clf()

mplt.show()
