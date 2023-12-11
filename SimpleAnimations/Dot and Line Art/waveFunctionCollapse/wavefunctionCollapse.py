import numpy as np
import matplotlib.pyplot as mplt
from PIL import Image

def clearGrid():
    global grid
    grid = []
    opt =  [list(range(0, len(tiles), 1))][0]
    for x in range(DIM**2):
        grid.append(cell(opt))
        grid[x].options = opt
        indexGrid.append(x)

def checkValid(arr, valid):
    indexesToDelete = []
    for i in range(len(arr) - 1, -1, -1):
        if( arr[i] not in valid ):
            indexesToDelete.append(i)
    for index in sorted(indexesToDelete, reverse=True):
        del arr[index]

class cell( object ):
  def __init__( self, value ):
    self.collapsed = False
    self.options = list(value)
   
def compareEdge(a, b):
  return int( a == b[::-1] )
 
class Tile( object ):
    def __init__(self, image, edges):
        self.image = image
        self.edges = edges
        self.up = []
        self.right = []
        self.down = []
        self.left = []
 
    def analyze(self, tiles):
        for (i, tile) in enumerate(tiles):
            if( compareEdge(tile.edges[2], self.edges[0]) ):
                self.up.append(i)
            if( compareEdge(tile.edges[3], self.edges[1]) ):
                self.right.append(i)
            if( compareEdge(tile.edges[0], self.edges[2]) ):
                self.down.append(i)
            if( compareEdge(tile.edges[1], self.edges[3]) ):
                self.left.append(i)
    
    def rotate(self, num):
        newImage = np.rot90(self.image, k=num)
        newEdges = []
        lenEdges = len(self.edges)
        #print(self.edges, lenEdges)
        for i in range(lenEdges):
            #print((i - num + lenEdges)%lenEdges)
            newEdges.append(self.edges[(i - num + lenEdges)%lenEdges])
        return Tile(newImage, newEdges)

def calculateEntropy():
    global DIM, grid
   
    nextGrid = []
    for j in range(DIM):
      for i in range(DIM):
        index = i + j * DIM
        if(grid[index].collapsed == True):
            nextGrid.append( grid[index] )
        else:
            options = [list(range(0, len(tiles), 1))][0]

            if( j > 0 ):
                up = grid[i + (j - 1) * DIM]
                validOptions = []
                for option in up.options:
                    for idxs in tiles[option].down:
                        validOptions.append( idxs )
                validOptions = list(set(validOptions))
                checkValid(options, validOptions)              
            if( i < DIM - 1 ):
                right = grid[i + 1 + j * DIM]
                validOptions = []
                for option in right.options:
                    for idxs in tiles[option].left:
                        validOptions.append( idxs )
                validOptions = list(set(validOptions))
                checkValid(options, validOptions)
            if( j < DIM - 1 ):
                down = grid[i + (j + 1) * DIM]
                validOptions = []
                for option in down.options:
                    for idxs in tiles[option].up:
                        validOptions.append( idxs )
                validOptions = list(set(validOptions))
                checkValid(options, validOptions)
            if( i > 0 ):
                left = grid[i - 1 + j * DIM]
                validOptions = []
                for option in left.options:
                    for idxs in tiles[option].right:
                        validOptions.append( idxs )
                validOptions = list(set(validOptions))
                checkValid(options, validOptions)

            nextCell = cell(options)
            nextCell.options = options
            nextGrid.append( nextCell )
           
    #print("nextGrid Length", len(nextGrid))    
    grid = list(nextGrid)



tileImages = []
#tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/selfMadeWfcPhotos/GroundTiles/Desert/0.png").convert("RGBA")))
#tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/selfMadeWfcPhotos/GroundTiles/Desert/1.png").convert("RGBA")))
#tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/selfMadeWfcPhotos/GroundTiles/Desert/2.png").convert("RGBA")))
#tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/selfMadeWfcPhotos/GroundTiles/Desert/3.png").convert("RGBA")))
#tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/selfMadeWfcPhotos/GroundTiles/Desert/4.png").convert("RGBA")))
#tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/selfMadeWfcPhotos/GroundTiles/Desert/5.png").convert("RGBA")))
#tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/selfMadeWfcPhotos/GroundTiles/Desert/6.png").convert("RGBA")))
tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/selfMadeWfcPhotos/GroundTiles/Desert/7.png").convert("RGBA")))
tileImages = np.array(tileImages)

tiles = []
tiles.append( Tile(tileImages[0], ["BBB", "BBB", "BBB", "BBB"]))
#tiles.append( Tile(tileImages[1], ["BBB", "BBB", "BBB", "BBB"]))
#tiles.append( Tile(tileImages[2], ["BBB", "BBB", "BBB", "BBB"]))
#tiles.append( Tile(tileImages[3], ["BBB", "BBB", "BBB", "BBB"]))
#tiles.append( Tile(tileImages[4], ["BBB", "BBB", "BBB", "BBB"]))
#tiles.append( Tile(tileImages[5], ["BBB", "BBB", "BBB", "BBB"]))
#tiles.append( Tile(tileImages[6], ["BBB", "BBB", "BBB", "BBB"]))
#for i in [0, 3]:
#    for j in range(1, 4):
#      tempTile = tiles[i].rotate(j)
#      tiles.append(tempTile)  
for tile in tiles:
    tile.analyze(tiles)
    #print(tile.up, tile.down, tile.left, tile.right)

#width and heighth of the map area
DIM = 4
#establish grid and place all options to viable (max entropy) by creating a list of numbers from 0 - len(tiles)
grid = []; indexGrid = []; clearGrid()
#print(indexGrid)

numIterations = DIM**2; restartCount = 0
for iters in range(numIterations):
    print("iters", iters)

    gridCopy = list(zip(list(grid), list(indexGrid)))
    indexesToDelete = []
    for item in (gridCopy):
        if( item[0].collapsed == True ):
            #print("here", item[1])
            indexesToDelete.append(item[1])
    for index in sorted(indexesToDelete, reverse=True):
        del gridCopy[index]
    if(len(gridCopy) == 0):
       print("lengridCopy == 0")
       break
    #print(gridCopy)

    gridCopy = sorted(gridCopy, key=lambda x: len(x[0].options))

    length = len(gridCopy[0][0].options)
    stopIndex = 0
    for i in range(1, len(gridCopy)):
       if(len(gridCopy[i][0].options) > length):
            stopIndex = i
            break
    if(stopIndex > 0):
        #print("stopIndex", stopIndex)
        del gridCopy[stopIndex:]
    #print("len GridCopy", len(gridCopy))

    cellToCollapse = np.random.randint(0, len(gridCopy))
    indexToCollapse = gridCopy[cellToCollapse][1]
    grid[indexToCollapse].collapsed = True
    if(len(grid[indexToCollapse].options) > 0):
        optionToPick = np.random.randint(0, len(grid[indexToCollapse].options))
        grid[indexToCollapse].options = [grid[indexToCollapse].options[optionToPick]]
    else:
       print("pick == None")
       clearGrid()
       iters = 0

    calculateEntropy()
   
#print(len(gridCopy))
#for cell in grid:
#    print(cell.options)

idx = 0
gridX = DIM; gridY = DIM
dim = [gridX*tileImages.shape[1], gridY*tileImages.shape[2], tileImages.shape[3]]
imgToPlot = np.zeros(dim, dtype=np.int64)
for i in range(gridX):
    for j in range(gridY):
        idxToPlot = grid[idx].options[0]; #print(idxToPlot)
        imgToPlot[j*tileImages.shape[1]:(j+1)*tileImages.shape[1], i*tileImages.shape[2]:(i+1)*tileImages.shape[2], :] = tiles[idxToPlot].image
        idx += 1

mplt.figure(figsize=(8,8))
mplt.tight_layout()
mplt.axis('off')
mplt.imshow(imgToPlot)
mplt.show()