import numpy as np
import matplotlib.pyplot as mplt
from PIL import Image

def clearGrid():
    global DIM, grid, tiles, indexGrid
    grid = []
    opt =  [list(range(0, len(tiles), 1))][0]
    for j in range(DIM):
      for i in range(DIM):
        index = i + (j * DIM)
        grid.append(cell(opt, index))
        indexGrid.append(index)
    for j in range(DIM):
      for i in range(DIM):
            index = i + (j * DIM)
            if( j > 0 ):
                up = grid[i + ((j - 1) * DIM)]
                grid[index].addNeighbor(up, 0)
            if( i < DIM - 1 ):
                right = grid[(i + 1) + (j * DIM)]
                grid[index].addNeighbor(right, 1)
            if( j < DIM - 1 ):
                down = grid[i + ((j + 1) * DIM)]
                grid[index].addNeighbor(down, 2)    
            if( i > 0 ):
                left = grid[(i - 1) + (j * DIM)]
                grid[index].addNeighbor(left, 3)
               
def checkValid(arr, valid):
        indexesToDelete = []
        for i in range(len(arr) - 1, -1, -1):
            if( arr[i] not in valid ):
                indexesToDelete.append(i)
        for index in sorted(indexesToDelete, reverse=True):
            del arr[index]

class cell( object ):

    def __init__( self, value, index ):
        self.collapsed = False
        self.options = list(value)
        self.index = index
        self.neighbors = [[], [], [], []]

    def addNeighbor(self, object, idx):
        self.neighbors[idx].append(object)

    def iterateNeighbors( self, caller, direction ):
        global seenArray

        if(not self.collapsed):
            self.updateEntropy(self, caller, direction)

        for j in range(4):
            for n in self.neighbors[j]:
                if(not n.collapsed):
                    n.updateEntropy(self, j)

    def updateEntropy(self, caller, direction):
       
        seenArray.append(self.index)
        validOptions = []
        for option in caller.options:
            for compatibleTile in tiles[option].compatabilities[direction]:
                validOptions.append(compatibleTile)

        checkValid(self.options, validOptions)
        print(self.index, self.options, caller.index, direction)
        if(len(self.options) == 0):
            startOver()

        for j in range(4):
            for n in self.neighbors[j]:
                if(n.index not in seenArray and not n.collapsed):
                    n.updateEntropy(self, j)

    def nonrecursiveCheck(self):
        validOptions = []
        for dir in range(4):
          for neighbor in self.neighbors[dir]:
            for option in neighbor.options:
                for compatibleTile in tiles[option].compatabilities[dir]:
                  validOptions.append(compatibleTile)
        checkValid(self.options, validOptions)
       
        if(len(self.options) == 0):
            startOver()
               
    def collapse(self, randomPick):
        global seenArray

        seenArray = [self.index]
        self.collapsed = True
        if(randomPick):
            self.nonrecursiveCheck()
            tileToChoose = np.random.choice(self.options)
            self.options = list([tileToChoose])
        else:
            None

        print("collapsing cell", self.index, "with option", self.options[0])
        self.iterateNeighbors(self, 0)

def compareEdge(a, b):
  return int( a == b[::-1] )
 
class Tile( object ):
    def __init__(self, image, edges):
        self.image = image
        self.edges = edges
        self.compatabilities = [[], [], [], []]
 
    def analyze(self, tiles):
        for (i, tile) in enumerate(tiles):
            if( compareEdge(tile.edges[2], self.edges[0]) ):              
                self.compatabilities[0].append(i)
            if( compareEdge(tile.edges[3], self.edges[1]) ):
                self.compatabilities[1].append(i)
            if( compareEdge(tile.edges[0], self.edges[2]) ):
                self.compatabilities[2].append(i)
            if( compareEdge(tile.edges[1], self.edges[3]) ):
                self.compatabilities[3].append(i)
   
    def rotate(self, num):
        newImage = np.rot90(self.image, k=num)
        newEdges = []
        lenEdges = len(self.edges)
        for i in range(lenEdges):
            newEdges.append(self.edges[(i - num + lenEdges)%lenEdges])
        return Tile(newImage, newEdges)

def startOver():
    global masterEntropyList, seenArray, indexGrid, grid
    print("##START OVER INITIATED##")
    print("##START OVER INITIATED##")
    grid = []; indexGrid = []; seenArray = []; masterEntropyList = []
    clearGrid()
    candidatesForCollapse = [list(range(0, DIM**2, 1))][0]
    idxOfRandomlyChosenCellToCollapse = np.random.choice(candidatesForCollapse)
    grid[idxOfRandomlyChosenCellToCollapse].collapse(randomPick=True)

DIM = 12
grid = []; indexGrid = []; seenArray = []
tileImages = []
tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/0.png").convert("RGBA")))
tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/1.png").convert("RGBA")))
tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/2.png").convert("RGBA")))
tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/3.png").convert("RGBA")))
tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/4.png").convert("RGBA")))
tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/5.png").convert("RGBA")))
tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/6.png").convert("RGBA")))
tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/7.png").convert("RGBA")))
tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/8.png").convert("RGBA")))
tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/9.png").convert("RGBA")))
tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/10.png").convert("RGBA")))
tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/11.png").convert("RGBA")))
tileImages.append(np.asarray(Image.open("/Users/shawnmilloway/Desktop/wfcPhotos/12.png").convert("RGBA")))
tileImages = np.array(tileImages)

#AAA BBB ACA ABA 
tiles = []
tiles.append( Tile(tileImages[0], ["BBB", "BBB", "BBB", "BBB"]) )
tiles.append( Tile(tileImages[1], ["AAA", "AAA", "AAA", "AAA"]) )
tiles.append( Tile(tileImages[2], ["AAA", "ACA", "AAA", "AAA"]) )
tiles.append( Tile(tileImages[3], ["AAA", "ADA", "AAA", "ADA"]) )
tiles.append( Tile(tileImages[4], ["BAA", "ACA", "AAB", "BBB"]) )
tiles.append( Tile(tileImages[5], ["BAA", "AAA", "AAA", "AAB"]) )
tiles.append( Tile(tileImages[6], ["AAA", "ACA", "AAA", "ACA"]) )
tiles.append( Tile(tileImages[7], ["ADA", "ACA", "ADA", "ACA"]) )
tiles.append( Tile(tileImages[8], ["ADA", "AAA", "ACA", "AAA"]) )
tiles.append( Tile(tileImages[9], ["ACA", "ACA", "AAA", "ACA"]) )
tiles.append( Tile(tileImages[10], ["ACA", "ACA", "ACA", "ACA"]) )
tiles.append( Tile(tileImages[11], ["ACA", "ACA", "AAA", "AAA"]) )
tiles.append( Tile(tileImages[12], ["AAA", "ACA", "AAA", "ACA"]) )
for tile in tiles:
    tile.analyze(tiles)
    print(tile.compatabilities)

masterEntropyList = []
clearGrid()
grid[DIM].collapse(randomPick=True)
print(masterEntropyList, seenArray)

maxIters = 468
for itr in range(maxIters):
    masterEntropyList = []
    for c in grid:
        if( not c.collapsed ):
            if(len(c.options) > 1):
                masterEntropyList.append([c.index, len(c.options)])
            elif(len(c.options) == 1):
                c.collapse(randomPick=False)

    for idx, entropy in masterEntropyList:
        if(entropy == 1):
            grid[idx].collapse(0)
    if(len(masterEntropyList) > 0):
        masterEntropyList = list(sorted(masterEntropyList, key=lambda x: x[1]))
    else:
        masterEntropyList = []
        for c in grid:
          if(len(c.options) > 1):
            masterEntropyList.append([c.index, len(c.options)])
        if(len(masterEntropyList) > 0):
          None
        else:
          print("master entropy list empty")
          break
    minimumEntropy = masterEntropyList[0][1]
    candidatesForCollapse = []
    for idx, entropy in masterEntropyList:
        if(entropy == minimumEntropy):
            candidatesForCollapse.append(idx)
    print("candidatesForCollapse", candidatesForCollapse, "masterEntropyList", masterEntropyList)
    idxOfRandomlyChosenCellToCollapse = np.random.choice(candidatesForCollapse)
    grid[idxOfRandomlyChosenCellToCollapse].collapse(randomPick=True)

idx = 0
gridX = DIM; gridY = DIM
dim = [gridX*tileImages.shape[1], gridY*tileImages.shape[2], tileImages.shape[3]]
imgToPlot = np.zeros(dim, dtype=np.int64)
for j in range(gridX):
    for i in range(gridY):
        index = i + (j * DIM)
        if(grid[index].collapsed):
            idxToPlot = grid[index].options[0]; print(grid[index].index, grid[index].options)
        else:
            idxToPlot = 0
        imgToPlot[j*tileImages.shape[1]:(j+1)*tileImages.shape[1], i*tileImages.shape[2]:(i+1)*tileImages.shape[2], :] = tiles[idxToPlot].image

mplt.figure(figsize=(8,8))
mplt.tight_layout()
mplt.axis('off')
mplt.imshow(imgToPlot)
mplt.show()