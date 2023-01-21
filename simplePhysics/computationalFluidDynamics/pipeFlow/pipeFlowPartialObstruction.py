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

stepHeightNPoints = 7; stepWidthNPoints = 60

nPressuePoissonIterations = 50

nPointsY = 15; aspectRatio = 10
cellLength = 1.0/(nPointsY - 1); nPointsX = (nPointsY - 1) * aspectRatio + 1
xRange = np.linspace(0.0, 1.0 * aspectRatio, num=nPointsX); yRange = np.linspace(0.0, 1.0, nPointsY)
coordinatesX, coordinatesY = np.meshgrid(xRange, yRange)

#yAxis, xAxis coordinates
velocityXPrevious = np.ones([nPointsY + 1, nPointsX])
velocityXPrevious[:(stepHeightNPoints+1), :] = 0.0
#top edge domain
velocityXPrevious[-1, :] = -velocityXPrevious[-2, :]
#step top edge
velocityXPrevious[stepHeightNPoints, 1:stepWidthNPoints] = -velocityXPrevious[stepHeightNPoints+1, 1:stepWidthNPoints]
#step right edge
velocityXPrevious[1:stepHeightNPoints+1, stepWidthNPoints] = 0.0
#bottom edge domain
velocityXPrevious[0, stepWidthNPoints+1:-1] = -velocityXPrevious[1, stepWidthNPoints+1:-1]
#step interior values
velocityXPrevious[:stepHeightNPoints, :stepWidthNPoints] = 0.0
#array allocation
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
    #inflow
    velocityXTentative[stepHeightNPoints+1:-1, 0] = 1.0
    #outflow
    inflowMassRateTent = np.sum(velocityXTentative[stepHeightNPoints+1:-1, 0])
    outflowMassRateTent = np.sum(velocityXTentative[1:-1, -2])
    velocityXTentative[1:-1, -1] = velocityXTentative[1:-1, -2] * (inflowMassRateTent/outflowMassRateTent)
    #step top edge
    velocityXTentative[stepHeightNPoints, 1:stepWidthNPoints] = -velocityXTentative[stepHeightNPoints+1, 1:stepWidthNPoints]
    #step right edge
    velocityXTentative[1:stepHeightNPoints+1, stepWidthNPoints] = 0.0
    #top domain
    velocityXTentative[0, :] = -velocityXTentative[1, :]
    #bottom domain
    velocityXTentative[0, stepWidthNPoints+1:-1] = -velocityXTentative[1, stepWidthNPoints+1:-1]
    #set u velocities inside step to 0.0
    velocityXTentative[:stepHeightNPoints, :stepWidthNPoints] = 0.0

    ##############################
    ##############################

    #update interior of V velocity
    diffusionY = kinematicViscosity * fivePointStencil(velocityYPrevious, cellLength)

    convectionXTerm = (velocityXPrevious[2:-1, 1:] + velocityXPrevious[2:-1, :-1] + velocityXPrevious[1:-2, 1:] + velocityXPrevious[1:-2, :-1])/4.0
    convectionY = (convectionXTerm * centralDifferenceX(velocityYPrevious, cellLength)) + centralDifferenceY(velocityYPrevious**2.0, cellLength)

    pressureGradientY = (pressurePrev[2:-1, 1:-1] - pressurePrev[1:-2, 1:-1])/cellLength

    velocityYTentative[1:-1, 1:-1] = velocityYPrevious[1:-1, 1:-1] + (timeStepLength * (-pressureGradientY + diffusionY - convectionY))

    #boundary conditions Y
    #inflow
    velocityYTentative[stepHeightNPoints+1:-1, 0] = -velocityYTentative[stepHeightNPoints+1:-1, 1]
    #outflow
    velocityYTentative[1:-1, -1] = velocityYTentative[1:-1, -2]
    #step top edge
    velocityYTentative[stepHeightNPoints, 1:stepWidthNPoints+1] = 0.0
    #step right edge
    velocityYTentative[1:stepHeightNPoints+1, stepWidthNPoints] = -velocityYTentative[1:stepHeightNPoints+1, stepWidthNPoints+1]
    #top domain
    velocityYTentative[-1, :] = 0.0
    #bottom domain
    velocityYTentative[-1, stepWidthNPoints+1:] = 0.0
    #set u velocities inside step to 0.0
    velocityYTentative[:stepHeightNPoints, :stepWidthNPoints] = 0.0

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
        #inflow
        pressureCorrectionNext[stepHeightNPoints+1:-1, 0] = pressureCorrectionNext[stepHeightNPoints+1:-1, 1]
        #outflow
        pressureCorrectionNext[1:-1, 1] = -pressureCorrectionNext[1:-1, -2]
        #step top edge
        pressureCorrectionNext[stepHeightNPoints, 1:stepWidthNPoints+1] = pressureCorrectionNext[stepHeightNPoints+1, 1:stepWidthNPoints+1]
        #step right edge
        pressureCorrectionNext[1:stepHeightNPoints+1, stepWidthNPoints] = pressureCorrectionNext[1:stepHeightNPoints+1, stepWidthNPoints+1]
        #bottom domain
        pressureCorrectionNext[0, stepWidthNPoints+1:-1] = pressureCorrectionNext[1, stepWidthNPoints+1:-1]
        #top 
        pressureCorrectionNext[-1, :] = pressureCorrectionNext[-2, :]
        #set all pressure correction values inside step to 0.0
        pressureCorrectionNext[:stepHeightNPoints, stepWidthNPoints] = 0.0

        pressureCorrectionPrev = np.copy( pressureCorrectionNext )

    pressureNext = pressurePrev + pressureCorrectionNext

    pressureCorrectionGradientX = (pressureCorrectionNext[1:-1, 2:-1] - pressureCorrectionNext[1:-1, 1:-2])/cellLength
    velocityXNext[1:-1, 1:-1] = velocityXTentative[1:-1, 1:-1] - (timeStepLength*pressureCorrectionGradientX)

    pressureCorrectionGradientY = (pressureCorrectionNext[2:-1, 1:-1] - pressureCorrectionNext[1:-2, 1:-1])/cellLength
    velocityYNext[1:-1, 1:-1] = velocityYTentative[1:-1, 1:-1] - (timeStepLength*pressureCorrectionGradientY)

    #boundary conditions
    #boundary conditions X
    #inflow
    velocityXNext[stepHeightNPoints+1:-1, 0] = 1.0
    #outflow
    inflowMassRateTent = np.sum(velocityXNext[stepHeightNPoints+1:-1, 0])
    outflowMassRateTent = np.sum(velocityXNext[1:-1, -2])
    velocityXNext[1:-1, -1] = velocityXNext[1:-1, -2] * (inflowMassRateTent/outflowMassRateTent)
    #step top edge
    velocityXNext[stepHeightNPoints, 1:stepWidthNPoints] = -velocityXNext[stepHeightNPoints+1, 1:stepWidthNPoints]
    #step right edge
    velocityXNext[1:stepHeightNPoints+1, stepWidthNPoints] = 0.0
    #top domain
    velocityXNext[0, :] = -velocityXNext[1, :]
    #bottom domain
    velocityXNext[0, stepWidthNPoints+1:-1] = -velocityXNext[1, stepWidthNPoints+1:-1]
    #set u velocities inside step to 0.0
    velocityXNext[:stepHeightNPoints, :stepWidthNPoints] = 0.0

    inflowMassRateNext = np.sum(velocityXPrevious[1:-1, 0])
    outflowMassRateNext = np.sum(velocityXPrevious[1:-1, -2])

    #boundary conditions Y
    #inflow
    velocityYNext[stepHeightNPoints+1:-1, 0] = -velocityYNext[stepHeightNPoints+1:-1, 1]
    #outflow
    velocityYNext[1:-1, -1] = velocityYNext[1:-1, -2]
    #step top edge
    velocityYNext[stepHeightNPoints, 1:stepWidthNPoints+1] = 0.0
    #step right edge
    velocityYNext[1:stepHeightNPoints+1, stepWidthNPoints] = -velocityYNext[1:stepHeightNPoints+1, stepWidthNPoints+1]
    #top domain
    velocityYNext[-1, :] = 0.0
    #bottom domain
    velocityYNext[-1, stepWidthNPoints+1:] = 0.0
    #set u velocities inside step to 0.0
    velocityYNext[:stepHeightNPoints, :stepWidthNPoints] = 0.0

    velocityXPrevious = velocityXNext
    velocityYPrevious = velocityYNext
    pressurePrev = pressureNext

    if( i % plotEvery == 0.0 ):
        
        velocityXVertexCentered = (velocityXNext[1:, :] + velocityXNext[:-1, :])/2.0
        velocityYVertexCentered = (velocityYNext[:, 1:] + velocityYNext[:, :-1])/2.0
        
        velocityXVertexCentered[:stepHeightNPoints+1, :stepWidthNPoints+1] = 0.0
        velocityYVertexCentered[:stepHeightNPoints+1, :stepWidthNPoints+1] = 0.0
        
        mplt.contourf(coordinatesX, coordinatesY, velocityXVertexCentered, levels=10, cmap='ocean')
        mplt.quiver(coordinatesX[:, ::6], coordinatesY[:, ::6], velocityXVertexCentered[:, ::6], velocityYVertexCentered[:, ::6])

        mplt.draw()
        mplt.pause(0.05)
        mplt.clf()

mplt.figure()
mplt.streamplot(coordinatesX, coordinatesY, velocityXVertexCentered, velocityYVertexCentered)

mplt.show()

