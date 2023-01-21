import numpy as np
import matplotlib.pyplot as mplt

def fivePointStencil(arrayData, cellLength):
    # (y, x) coordinates instead of (x, y)
    return (  arrayData[1:-1, 2:] + arrayData[2:, 1:-1]  
            + arrayData[1:-1, :-2] + arrayData[:-2, 1:-1] - 4.0 * arrayData[1:-1, 1:-1] )/(cellLength**2.0)

def centralDifferenceX(arrayData, cellLength):
    # (y, x) coordinates instead of (x, y)
    return (arrayData[1:-1, 2:] - arrayData[1:-1, :-2])/(2.0 * cellLength)

def centralDifferenceY(arrayData, cellLength):
    # (y, x) coordinates instead of (x, y)
    return (arrayData[2:, 1:-1] - arrayData[:-2, 1:-1])/(2.0 * cellLength)

kinematicViscosity = 0.01
timeStepLength = 0.0003; nTimeSteps = 6000; plotEvery = 100

nPressuePoissonIterations = 50

nPointsY = 15; aspectRatio = 10
cellLength = 1.0/(nPointsY - 1); nPointsX = (nPointsY - 1) * aspectRatio + 1
xRange = np.linspace(0.0, 1.0 * aspectRatio, num=nPointsX); yRange = np.linspace(0.0, 1.0, nPointsY)
coordinatesX, coordinatesY = np.meshgrid(xRange, yRange)

#yAxis, xAxis coordinates
velocityXPrevious = np.ones([nPointsY + 1, nPointsX])
velocityXPrevious[0, :] = -velocityXPrevious[1, :]; velocityXPrevious[-1, :] = -velocityXPrevious[-2, :]
velocityXTentative = np.zeros_like(velocityXPrevious); velocityXNext = np.zeros_like(velocityXPrevious)

velocityYPrevious = np.zeros([nPointsY, nPointsX + 1])
velocityYTentative = np.zeros_like(velocityYPrevious); velocityYNext = np.zeros_like(velocityYPrevious)

pressurePrev = np.zeros([nPointsY + 1, nPointsX + 1])

for i in range(nTimeSteps):

    #update interior of U velocity
    diffusionX = kinematicViscosity * fivePointStencil(velocityXPrevious, cellLength)

    convectionYTerm = ((velocityYPrevious[1:, 1:-2] + velocityYPrevious[1:, 2:-1] + velocityYPrevious[:-1, 1:-2] + velocityYPrevious[:-1, 2:-1])/4.0) 
    convectionX = centralDifferenceX(velocityXPrevious**2.0, cellLength) + (convectionYTerm * centralDifferenceY(velocityXPrevious, cellLength))
    
    pressureGradientX = (pressurePrev[1:-1, 2:-1] - pressurePrev[1:-1, 1:-2])/cellLength
    
    velocityXTentative[1:-1, 1:-1] = (velocityXPrevious[1:-1, 1:-1] + (timeStepLength*(-pressureGradientX + diffusionX - convectionX)))

    #boundary conditions X
    #left
    velocityXTentative[1:-1, 0] = 1.0
    #right
    velocityXTentative[1:-1, -1] =  velocityXTentative[1:-1, -2]
    #top
    velocityXTentative[0, :] = -velocityXTentative[1, :]
    #bottom
    velocityXTentative[-1, :] = -velocityXTentative[-2, :]

    ##############################
    ##############################

    #update interior of V velocity
    diffusionY = kinematicViscosity * fivePointStencil(velocityYPrevious, cellLength)

    convectionXTerm = (velocityXPrevious[2:-1, 1:] + velocityXPrevious[2:-1, :-1] + velocityXPrevious[1:-2, 1:] + velocityXPrevious[1:-2, :-1])/4.0
    convectionY = (convectionXTerm * centralDifferenceX(velocityYPrevious, cellLength)) + centralDifferenceY(velocityYPrevious**2.0, cellLength)

    pressureGradientY = (pressurePrev[2:-1, 1:-1] - pressurePrev[1:-2, 1:-1])/cellLength

    velocityYTentative[1:-1, 1:-1] = velocityYPrevious[1:-1, 1:-1] + (timeStepLength * (-pressureGradientY + diffusionY - convectionY))

    #boundary conditions Y
    #left
    velocityYTentative[1:-1, 0] = -velocityYTentative[1:-1, 1]
    #right
    velocityYTentative[1:-1, -1] = -velocityYTentative[1:-1, -2]
    #top
    velocityYTentative[0, :] = 0.0
    #bottom
    velocityYTentative[-1, :] = 0.0

    ##############################
    ##############################

    #divergence of interior - summed central differences of X and Y velocity components
    divergence = ((velocityXTentative[1:-1, 1:] - velocityXTentative[1:-1, :-1])/cellLength) + ((velocityYTentative[1:, 1:-1] - velocityYTentative[:-1, 1:-1])/cellLength)
    
    #density would appear in ppRHS if density != 1
    pressurePoissonRHS = divergence/timeStepLength
    #poisson problem - jacobi iteration
    pressureCorrectionPrev = np.zeros_like(pressurePrev)
    for _ in range(nPressuePoissonIterations):
        
        pressureCorrectionNext = np.zeros_like(pressureCorrectionPrev)
        
        #algebraically manipulated five-point stencil
        pressureCorrectionNext[1:-1, 1:-1] = 0.25 * (pressureCorrectionPrev[1:-1, 2:] + pressureCorrectionPrev[2:, 1:-1] + pressureCorrectionPrev[1:-1, :-2] + pressureCorrectionPrev[:-2, 1:-1] - (cellLength**2.0)*pressurePoissonRHS)

        #apply boundary conditions
        #left - neumann
        pressureCorrectionNext[1:-1, 0] = pressureCorrectionNext[1:-1, 1]
        #right - dirichlet
        pressureCorrectionNext[1:-1, -1] = -pressureCorrectionNext[1:-1, -2]
        #bottom
        pressureCorrectionNext[0, :] = pressureCorrectionNext[1, :]
        #top 
        pressureCorrectionNext[-1, :] = pressureCorrectionNext[-2, :]

        pressureCorrectionPrev = np.copy( pressureCorrectionNext )

    pressureNext = pressurePrev + pressureCorrectionNext

    pressureCorrectionGradientX = (pressureCorrectionNext[1:-1, 2:-1] - pressureCorrectionNext[1:-1, 1:-2])/cellLength
    velocityXNext[1:-1, 1:-1] = velocityXTentative[1:-1, 1:-1] - (timeStepLength*pressureCorrectionGradientX)

    pressureCorrectionGradientY = (pressureCorrectionNext[2:-1, 1:-1] - pressureCorrectionNext[1:-2, 1:-1])/cellLength
    velocityYNext[1:-1, 1:-1] = velocityYTentative[1:-1, 1:-1] - (timeStepLength*pressureCorrectionGradientY)

    #boundary conditions
    #boundary conditions X
    #left
    velocityXNext[1:-1, 0] = 1.0
    #right
    velocityXNext[1:-1, -1] =  velocityXNext[1:-1, -2]
    #top
    velocityXNext[0, :] = -velocityXNext[1, :]
    #bottom
    velocityXNext[-1, :] = -velocityXNext[-2, :]

    inflowMassRateNext = np.sum(velocityXPrevious[1:-1, 0])
    outflowMassRateNext = np.sum(velocityXPrevious[1:-1, -2])

    #boundary conditions Y
    #left
    velocityYNext[1:-1, 0] = -velocityYNext[1:-1, 1]
    #right
    velocityYNext[1:-1, -1] = -velocityYNext[1:-1, -2] * inflowMassRateNext/outflowMassRateNext
    #top
    velocityYNext[0, :] = 0.0
    #bottom
    velocityYNext[-1, :] = 0.0

    velocityXPrevious = velocityXNext
    velocityYPrevious = velocityYNext
    pressurePrev = pressureNext

    inflowMassRateNext = np.sum(velocityXPrevious[1:-1, 0])
    outflowMassRateNext = np.sum(velocityXPrevious[1:-1, -1])


    if( i % plotEvery == 0.0 ):
        
        velocityXVertexCentered = (velocityXNext[1:, :] + velocityXNext[:-1, :])/2.0
        velocityYVertexCentered = (velocityYNext[:, 1:] + velocityYNext[:, :-1])/2.0
        
        mplt.contourf(coordinatesX, coordinatesY, velocityXVertexCentered, levels=10, cmap='ocean')
        mplt.quiver(coordinatesX[:, ::6], coordinatesY[:, ::6], velocityXVertexCentered[:, ::6], velocityYVertexCentered[:, ::6])

        mplt.draw()
        mplt.pause(0.05)
        mplt.clf()

mplt.show()

