import numpy as np
import matplotlib.pyplot as mplt

def centralDifferenceX(f):
  global elementLength
  diff = np.zeros_like(f)
  diff[1:-1, 1:-1] = (f[1:-1, 2:] - f[1:-1, 0:-2])/(2.0*elementLength)
  return diff

def centralDifferenceY(f):
  global elementLength
  diff = np.zeros_like(f)
  diff[1:-1, 1:-1] = (f[2:,1:-1] - f[0:-2, 1:-1])/(2.0*elementLength)
  return diff

def laplace(f):
  global elementLength
  diff = np.zeros_like(f)
  diff[1:-1, 1:-1] = (f[1:-1, 0:-2] + f[0:-2, 1:-1] - 4.0*f[1:-1,1:-1] +
  f[1:-1, 2:] + f[2:, 1:-1])/(elementLength**2.0)
  return diff

nPoints = 41
domainSize = 1.0
nIterations = 30
timeStepLength = 0.001
kinematicViscosity = 0.1
fluidDensity = 1.0
horizontalVelocityTop = 1.0

nPressurePoissonIterations = 50

elementLength = domainSize/(nPoints - 1)
xAxis = np.linspace(0.0, domainSize, nPoints); yAxis = np.linspace(0.0, domainSize, nPoints); X, Y = np.meshgrid(xAxis, yAxis)
uPrev = np.zeros_like(X); vPrev = np.zeros_like(X); pPrev = np.zeros_like(X)

maxPossibleTimeStep = (0.5 * elementLength**2.0 / kinematicViscosity)
if(timeStepLength > 0.5*maxPossibleTimeStep):
  print("stability is not guaranteed")

for _ in range(nIterations):

  dUPrevdX = centralDifferenceX(uPrev); dUPrevdY = centralDifferenceY(uPrev)
  dVPrevdX = centralDifferenceX(vPrev); dVPrevdY = centralDifferenceY(vPrev)
  laplaceUPrev = laplace(uPrev); laplaceVPrev = laplace(vPrev)

  uGuess = uPrev + timeStepLength*(-((uPrev * dUPrevdX) + (vPrev *
dUPrevdY)) + kinematicViscosity * laplaceUPrev)
  vGuess = vPrev + timeStepLength*(-((uPrev * dVPrevdX) + (vPrev *
dVPrevdY)) + kinematicViscosity * laplaceVPrev)

  #dirichlet boundary conditions for pressure and velocity
  uGuess[0, :] = 0.0; uGuess[:, 0] = 0.0; uGuess[:, -1] = 0.0
  uGuess[-1, :] = horizontalVelocityTop

  vGuess[0, :] = 0.0; vGuess[:, 0] = 0.0; vGuess[:, -1] = 0.0; vGuess[-1, :] = 0.0

  dUGuessDX = centralDifferenceX(uGuess); dVGuessDY = centralDifferenceY(vGuess)
  RHS = fluidDensity/timeStepLength * (dUGuessDX + dVGuessDY)

  for _ in range(nPressurePoissonIterations):
    pNext = np.zeros_like(pPrev)
    pNext[1:-1, 1:-1] = 0.25 * ((pPrev[1:-1, 0:-2] + pPrev[0:-2, 1:-1] + pPrev[1:-1, 2:] + pPrev[2:, 1:-1]) - (elementLength**2.0) * RHS[1:-1, 1:-1])

    #pressure boundary conditions = neumann boundary everywhere except for the "lid" (top)
    pNext[:, -1] = pNext[:, -2]; pNext[0, :] = pNext[1, :]; pNext[:, 0] = pNext[:, 1]; pNext[-1, :] = 0.0
    pPrev = pNext

  dPNextDX = centralDifferenceX(pNext); dPNextDY = centralDifferenceY(pNext)
  uNext = uGuess - timeStepLength/fluidDensity * dPNextDX
  vNext = vGuess - timeStepLength/fluidDensity * dPNextDY

  uNext[0, :] = 0.0; uNext[:, 0] = 0.0; uNext[:, -1] = 0.0
  uNext[-1, :] = horizontalVelocityTop

  vNext[0, :] = 0.0; vNext[:, 0] = 0.0; vNext[:, -1] = 0.0; vNext[-1, :] = 0.0

  uPrev = uNext; vPrev = vNext; pPrev = pNext

fig, ax = mplt.subplots(1)
ax.contourf(X, Y, pNext)
#ax.quiver(X, Y, uNext, vNext, color='black')
ax.streamplot(X, Y, uNext, vNext, color='black')
mplt.show()