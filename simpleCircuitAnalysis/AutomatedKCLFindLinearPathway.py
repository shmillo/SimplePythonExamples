class Node( object ):

    neighbor = []
    numberOfNeighbors = 0
    hasVisited = 0

    def __init__( self, name ):
        self.name = name


    def setNeighbors( self, *neighborList ):

        self.numberOfNeighbors = len( neighborList )

        for Node in neighborList:

            self.neighbor.append( Node )
    

    def getSpecificNeighbor( self, neighborNumber ):

        if neighborNumber < self.numberOfNeighbors:

            return self.neighbor[neighborNumber]
  

v1 = Node( "v1" )
v2 = Node( "v2" )
v3 = Node( "v3" )
v4 = Node( "v4" )

v1.setNeighbors( v2 )
v2.setNeighbors( v1, v4 )
v4.setNeighbors( v2, v3 )
v3.setNeighbors( v4 )

v1.hasVisited = 1
print( v1.name )

for Node in v1.neighbor:

    for Node in Node.neighbor:

       if Node.hasVisited == 0:

            print( Node.name )
            Node.hasVisited = 1
