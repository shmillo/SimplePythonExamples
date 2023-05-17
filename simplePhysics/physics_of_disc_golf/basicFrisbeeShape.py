import numpy as np
import matplotlib.pyplot as mplt

nx = 100; ny = 100

arcHeightOne = 10.0
arcBeginningPointOne = nx * 0.15; arcEndingPointOne = nx * 0.95
arcLengthInGridPointsOne = int(arcEndingPointOne - arcBeginningPointOne)
arcWidthOne = arcLengthInGridPointsOne

arcGeneratorPointsOne = np.linspace(-arcWidthOne, arcWidthOne, arcLengthInGridPointsOne)

arcPointsOne = arcHeightOne * (1.0 - (arcGeneratorPointsOne**2.0/arcWidthOne**2.0))**0.5
arcPointsXOne = np.linspace(arcBeginningPointOne, arcEndingPointOne, arcLengthInGridPointsOne)

mplt.plot(arcPointsXOne, arcPointsOne, c='black')

arcHeightTwo = arcHeightOne - 3.0
arcBeginningPointTwo = nx * 0.2; arcEndingPointTwo = nx * 0.9
arcLengthInGridPointsTwo = int(arcEndingPointTwo - arcBeginningPointTwo)
arcWidthTwo = arcLengthInGridPointsTwo

arcGeneratorPointsTwo = np.linspace(-arcWidthTwo, arcWidthTwo, arcLengthInGridPointsTwo)

arcPointsTwo = arcHeightTwo * (1.0 - (arcGeneratorPointsTwo**2.0/arcWidthTwo**2.0))**0.5
arcPointsXTwo = np.linspace(arcBeginningPointTwo, arcEndingPointTwo, arcLengthInGridPointsTwo)

mplt.plot(arcPointsXTwo, arcPointsTwo, c='black')

numConnectorPoints = 10
connectorPointsXOne = np.linspace(arcBeginningPointOne, arcBeginningPointTwo, numConnectorPoints)
connectorPointsXTwo = np.linspace(arcEndingPointOne, arcEndingPointTwo, numConnectorPoints)

mplt.plot(connectorPointsXOne, np.zeros_like(connectorPointsXOne), c='black')
mplt.plot(connectorPointsXTwo, np.zeros_like(connectorPointsXOne), c='black')

mplt.ylim(-5, 40)
mplt.xlim(0, nx)
mplt.show()