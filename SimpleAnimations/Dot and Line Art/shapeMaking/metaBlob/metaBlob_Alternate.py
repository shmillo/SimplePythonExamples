from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as mplt
import numpy as np

def clamp(v, mn, mx):
    return int(min(max(v,mn),mx))

def unitVector(data):
    return data/np.linalg.norm(data)

def unitVectorApprox(x, y):
    ax = abs(x); ay = abs(y)
    ratio = 0.0
    if(ax == 0.0 and ay == 0.0):
        ratio = 0.0
    else:
        ratio = 1.0/(max(ax, ay)) 
        ratio *= 1.29289 - (ax + ay) * ratio * 0.29289
    return [x*ratio, y*ratio]

class hashMap():

    def __init__(self, width, height):
        self.width = width; self.height = height
        self.grid = np.zeros([width,height])

        self.leftEdge = 0; self.rightEdge = self.width-1
        self.bottomEdge = 0; self.topEdge = self.height-1

    def clear(self):
        self.grid = np.zeros([self.width,self.height])

    def addToGrid(self, x, y, data):
        x = clamp(np.round_(x), 0, self.rightEdge); y = clamp(np.round_(y), 0, self.topEdge)
        self.grid[x][y] = data

    def readFromGridWithRadius(self, x, y, radius):
        left = max(int(np.round_(x - radius)), self.leftEdge); right = min(int(np.round_(x + radius)), self.rightEdge)
        bottom = max(int(np.round_(y - radius)), self.bottomEdge); top = min(int(np.round_(y + radius)), self.topEdge)
        result = []
        for i in range(left, right+1):
            for j in range(bottom, top+1):
                x = clamp(int(np.round_(i)), 0, self.rightEdge); y = clamp(int(np.round_(j)), 0, self.topEdge)
                result.append(self.grid[x][y])
        return result

def calculateVelocity(i, dt):
    global xPositions, yPositions, vx, vy

    pos = np.array([xPositions[0][i], yPositions[0][i]])
    old = np.array([xPositions[1][i], yPositions[1][i]])

    v = (pos - old) *  (1 / dt)
    vx[i] = v[0]; vy[i] = v[1]

def contain(i):
    global xPositions, yPositions, canvasRad, canvasRadSq, antiStickScalar

    pos = np.array([xPositions[0][i], yPositions[0][i]])
    lenSq = sum(pos**2.0)
    if(lenSq > canvasWidth):
        unitPos = pos/lenSq
        newPos = unitPos * canvasRad
        xPositions[0][i] = newPos[0]; yPositions[0][i] = newPos[1]
        antiStick = unitPos * (antiStickScalar * interactionRadius * dt)
        xPositions[1][i] += antiStick[0]; yPositions[1][i] += antiStick[1]

def containAlternate(i):
    global xPositions, yPositions, canvasRad, canvasRadSq, antiStickScalar
    
    xPos = xPositions[0][i]; yPos = yPositions[0][i]
    
    if(xPos >= canvasWidth or yPos >= canvasHeight):
        if(xPos >= canvasWidth):
            xPositions[0][i] = canvasWidth
        if(yPos >= canvasWidth):
            yPositions[0][i] = canvasWidth; 
        xPositions[1][i] += canvasWidth; yPositions[1][i] += canvasWidth

    if(xPos <= 0.0 or yPos <= 0.0):
        if(xPos <= 0.0):
            xPositions[1][i] = 0.0; 
        if(yPos <= 0.0):
            yPositions[1][i] = 0.0; 
        xPositions[1][i] += -canvasWidth; yPositions[1][i] += -canvasWidth

def getNeighboursWithGradients(i):
    global g, interactionRadius, interactionRadiusSq

    gridX = xPositions[0][i]; gridY = yPositions[0][i]
    
    radius = interactionRadius / canvasWidth
    results = hMap.readFromGridWithRadius(gridX, gridY, radius)
    
    neighbours = []
    for k in range(len(results)):
        n = int(results[k])
        if (i != n):
            G = gradient(i, n)
            if (G != 0): 
                g[n] = G; 
                neighbours.append(n)

    return neighbours

def updatePressure(i, neighbours):
    global stiffness, stiffnessNear, restDensity, p, pNear

    density = 0; nearDensity = 0

    for k in range(len(neighbours)):
        G = g[neighbours[k]]
        density += G * G
        nearDensity += G * G * G
 
    p[i] = stiffness * (density - restDensity)
    pNear[i] = stiffnessNear * nearDensity

def relax(i, neighbours, dt):
    global g, p, pNear, xPositions, yPositions

    pos = np.array([xPositions[0][i], yPositions[0][i]])
   
    for k in range(len(neighbours)):
        n = int(neighbours[k]); G = g[n]
        
        nPos = np.array([xPositions[0][n], yPositions[0][n]])
        magnitude = (p[i] * G) + (pNear[i] * G**2.0)

        nPos -= pos
        direction = unitVectorApprox(nPos[0], nPos[1]); direction = np.array(direction)
        force = direction * magnitude # * canvasWidth
        
        d = force * dt**2.0
        xPositions[0][i] += d[0] * -.5; yPositions[0][i] += d[1] * -.5
        xPositions[0][n] += d[0] * .5; yPositions[0][n] += d[1] * .5

def gradient(i, n):
    global interactionRadius, interactionRadiusSq, xPositions, yPositions

    particle = np.array([xPositions[0][i], yPositions[0][i]])
    neighbour = np.array([xPositions[0][n], yPositions[0][n]])
  
    returnValue = 0.0
    lsq = sum((particle - neighbour)**2.0)
    if (lsq < interactionRadiusSq): 
        distance = lsq**0.5
        returnValue = 1 - distance / interactionRadius
    return returnValue

def applyGlobalForces(i, dt):
    global force, userForce, vx, vy
    
    mass = 1.0

    force[0] += userForce[0][i]; force[1] += userForce[1][i]
    vx[i] += ((force[0]/mass) * dt); vy[i] += (force[1]/mass) * dt

def normalizeScalar(value, lowerAct, upperAct, lowerDes, upperDes):
    return lowerDes + (value - lowerAct) * (upperDes - lowerDes) / (upperAct - lowerAct)

def passOne():
    global particleCount, canvasWidth, canvasHeight, halfHeight, halfWidth, hMap, dt, xPositions, yPositions

    for i in range(particleCount):
        #set position history along both axes
        xPositions[1] = xPositions[0]; yPositions[1] = yPositions[0]

        #set forces. these can move particles, even from a resting state
        applyGlobalForces(i, dt)

        #apply forces to particle positions, yielding a new listing of particle locations
        xPositions[0][i] += vx[i] * dt; yPositions[0][i] += vy[i] * dt
        
        gridX = xPositions[0][i]; gridY = yPositions[0][i]

        #add points to the hash map
        hMap.addToGrid(gridX, gridY, i)

def passTwo():
    global particleCount, dt

    for i in range(particleCount):
        neighbors = getNeighboursWithGradients(i)
        updatePressure(i, neighbors)
        relax(i, neighbors, dt)

def passThree():
    global particleCount, dt
    for i in range(particleCount):
        containAlternate(i)
        #contain(i)
        calculateVelocity(i, dt)

def advanceTime(q):
    global numTimeSteps, force

    hMap.clear()
    passOne()
    passTwo() 
    passThree()
    
    ax.clear(); ax.set_facecolor('black')
    ax.set_xlim([canvasWidth * 0.25, canvasWidth * 0.75]); ax.set_ylim([canvasHeight * 0.25, canvasHeight * 0.75])
    ax.scatter(X, Y, hMap.grid, c='w')
    ax.scatter(X, Y, 2.0 * hMap.grid, c='w', alpha = 0.1)

dt = 1.0; particleCount = 400; canvasWidth = 600; canvasHeight = 600; gridCellsPerRow = canvasWidth
totalGridCells = canvasWidth * canvasHeight; halfWidth = canvasWidth * 0.5; halfHeight = canvasHeight * 0.5; hMap = hashMap(canvasWidth, canvasHeight)

xPositions = np.random.rand(2, particleCount); yPositions = np.random.rand(2, particleCount); xPositions *= canvasWidth; yPositions *= canvasWidth

#passOne
vx = np.zeros(particleCount); vy = np.zeros(particleCount); force = np.array([1.0, -1.0]); userForce = np.zeros([2, particleCount])
#passTwo
p = np.zeros(particleCount); pNear = np.zeros(particleCount); g = np.zeros(particleCount)
interactionRadius = 5; interactionRadiusSq = interactionRadius**2.0
stiffness = 100.0; stiffnessNear = 100.0; restDensity = 100.0
#passThree
#canvasRad = (canvasWidth*canvasHeight); 
canvasRad = 150.0; canvasRadSq = canvasRad**2.0; antiStickScalar = 1000.5

for i in range(len(userForce)):
    for j in range(2):
        userForce[j][i] = np.random.choice([-1.0, 1.0]) * 10.0 * np.random.rand()

numTimeSteps = 200
xAxis = np.arange(0, canvasWidth, 1); yAxis = np.arange(0, canvasHeight, 1); X, Y = np.meshgrid(xAxis, yAxis)

fig, (ax) = mplt.subplots(1, facecolor='black')
anim = FuncAnimation(fig, func=advanceTime, frames=np.linspace(0, numTimeSteps, num=numTimeSteps), interval=1)
anim.save("alternate_MetaBlob_T4.gif")
#mplt.show()