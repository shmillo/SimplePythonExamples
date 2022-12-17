from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as mplt
import numpy as np
import math

def integrate(dt, gravity):
  global nX, nY, v, s
  for i in range(1, nX):
    for j in range(1, nY - 1):
        if(s[i][j] != 0.0 and s[i][j-1] != 0.0):
            v[0][i][j] += gravity*dt

def incompressibility(numIts, dt):
  global nX, nY, s, h, u, v, p, overRelaxation, cp

  for iter in range(numIts):
    for i in range(1, nX - 1):
      for j in range(1, nY - 1):
        if( s[i][j] != 0.0 ):
          
            sx0 = s[i-1][j]; sx1 = s[i+1][j]
            sy0 = s[i][j-1]; sy1 = s[i][j+1]
            S = sx0 + sx1 + sy0 + sy1
            if(S != 0.0):
                div = u[0][i+1][j] - u[0][i][j] + v[0][i][j+1] - v[0][i][j]
                P = -div/S; P *= overRelaxation; p[i][j] += cp * P
                u[0][i][j] -= sx0 * P; u[0][i+1][j] += sx1 * P
                v[0][i][j] -= sy0 * P; v[0][i][j+1] += sy1 * P

def extrapolate():
  global u, v, nX, nY
  for i in range(nX):
    u[0][i][0] = u[0][i][1]; u[0][i][nY - 1] = u[0][i][nY - 2]
  for j in range(nY):
    v[0][0][j] = v[0][1][j]; v[0][nX-1][j] = v[0][nX - 2][j]

def sampleField(x, y, field):
  global nX, nY, h, u, v, m

  h1 = 1.0/h; h2 = 0.5 * h
  x = max(min(x, nX*h), h); y = max(min(y, nY*h),  h)

  dx = 0.0; dy = 0.0
  f = []
  if(field == 0):
    f = u; dy = h2 #'uField'
  elif(field == 1):
    f = v; dx = h2 #'vField'
  elif(field == 2):
    f = m; dx = h2; dy = h2 #'sField'
  f = np.array(f)

  x0 = int(min(math.floor((x - dx)*h1), nX - 1)); tx = ((x - dx) - x0*h) * h1; sx = 1.0 - tx
  x1 = int(min(x0 + 1, nX - 1))

  y0 = int(min(math.floor((y - dy)*h1), nY - 1)); ty = ((y - dy) - y0*h) * h1; sy = 1.0 - ty
  y1 = int(min(y0 + 1, nY - 1))

  val = (sx*sy*f[0][x0][y0]) + (tx*sy*f[0][x1][y0]) + (tx*ty*f[0][x1][y1]) + (sx*ty*f[0][x0][y1])
  return val

def avgU(i, j):
  global u
  return (0.25 * (u[0][i-1][j] + u[0][i][j] + u[0][i-1][j+1] + u[0][i][j+1]))

def avgV(i, j):
  global v
  return (0.25 * (v[0][i-1][j] + v[0][i][j] + v[0][i-1][j+1] + v[0][i][j+1]))

def advectVel(dt):
    global nX, nY, u, v, h

    h2 = h * 0.5
    u[1] = u[0]; v[1] = v[0]

    for i in range(1, nX):
        for j in range(1, nY):

            if(s[i][j] != 0.0 and s[i-1][j] != 0.0 and i < nX - 1 and j < nY - 1):
                x = i*h; y = j*h + h2
                U = u[0][i][j]; V = avgV(i,j)
                x = x - dt*U; y = y - dt*V
                U = sampleField(x, y, 0)
                u[1][i][j] = U

            if(s[i][j] != 0.0 and s[i][j-1] != 0.0 and i < nX - 1 and j < nY - 1):
                x = i*h + h2; y = j*h
                U = avgU(i, j); V = v[0][i][j]
                x = x - dt*U; y = y - dt*V
                V = sampleField(x, y, 1)
                v[1][i][j] = V

    u[0] = u[1]; v[0] = v[1]

def advectSmoke(dt):
    global nX, nY, h
    m[1] = m[0]; h2 = 0.5 * h
    for i in range(1, nX-1):
        for j in range(1, nY-1):
            if(s[i][j] != 0.0):
                U = 0.5 * (u[0][i][j] + u[0][i+1][j])
                V = 0.5 * (v[0][i][j] + v[0][i][j+1])
                x = i*h + h2 - dt*U; y = j*h + h2 - dt*V
                m[1][i][j] = sampleField(x, y, 2)
    m[0] = m[1]

def simulate(dt, gravity, numIters):
    global grid, p

    integrate(dt, gravity)
    
    p = np.zeros_like(grid)
    incompressibility(numIters, dt)

    extrapolate()
    advectVel(dt)
    advectSmoke(dt)

def grayConversion(image):
    height, width, channel = image.shape
    for i in range(0, height):
        for j in range(0, width):
            blueComponent = image[i][j][0]
            greenComponent = image[i][j][1]
            redComponent = image[i][j][2]
            grayValue = 0.07 * blueComponent + 0.72 * greenComponent + 0.21 * redComponent
            image[i][j] = (grayValue, grayValue, grayValue, image[i][j][3])
    return image
    
def getPressureColor():
    global p, nX, nY, pressureColor

    minVal = p.min(); maxVal = p.max()

    for i in range(nX):
        for j in range(nY):

            val = p[i][j]

            val = min(max(val, minVal), maxVal - 0.0001)

            d = maxVal - minVal
            if(d == 0.0):
                val = 0.5
            else:
                val = (val - minVal) / d
	
            M = 0.25
            num = math.floor(val / M)
            s = (val - num * M) / M

            r = 0.0; g = 0.0; b = 0.0
            if(num == 0):
                r = 0.0; g = s; b = 1.0
            elif(num == 1):
                r = 0.0; g = 1.0; b = 1.0-s
            elif(num == 2):
                r = s; g = 1.0; b = 0.0
            elif(num == 3):
                r = 1.0; g = 1.0 - s; b = 0.0
		
            pressureColor[i][j] = (255*r, 255*g, 255*b, 255)

def setObstacle(x, y, r):
    global nX, nY, s, u, v

    obstacleRadius = r; obstacleRadiusSquared = obstacleRadius**2.0
    forceLocationX = x; forceLocationY = y

    #vx = (0.0 - forceLocationX)/dt; vy = (0.0 - forceLocationY)/dt
    vx = 0.0; vy = 0.0
    for i in range(1, nX-2):
        for j in range(1, nY-2):
            dx = (i + 0.5) * h - forceLocationX; dy = (j + 0.5) * h - forceLocationY
            if(dx**2.0 + dy**2.0 < obstacleRadiusSquared):
                s[i][j] = 0.0
                m[0][i][j] = 1.0
                u[0][i][j] = vx; u[0][i+1][j] = vx
                v[0][i][j] = vy; v[0][i][j+1] = vy

def setPipe():
    global nY, nX, m
    pipeH = 0.1 * nY
    minJ = math.floor(0.5*nY - 0.5*pipeH); maxJ = math.floor(0.5*nY + 0.5*pipeH)
    for j in range(minJ, maxJ):
        for y in range(nY):
	        m[0][y][j] = 0.0

def setInVelocity():
    global nX, nY, s, u
    inVel = 2.0
    for i in range(nX):
        for j in range(nY):
            S = 1.0
            #if(i == 0 or i == nX-1 or j == 0):
            if(i == 0 or j == 0 or j == nY - 1):
                S = 0.0;	
            s[i][j] = S
            if(i == 1):
                u[0][i][j] = inVel
   
def animFunc(i):
    global X, Y, dt, gravity, p, v, s, u, m

    simulate(dt, gravity, 40)

    ax.clear(); ax.set_facecolor('black')
    
    getPressureColor();  
    grayMatrix = grayConversion(pressureColor/255.0)
    #for j in range(len(X)):
        #ax.scatter(X[j], Y[j], s = 20.0 * m[0][j], c=pressureColor[j]/255.0)
    #    ax.scatter(X[j], Y[j], s = 20.0 * m[0][j], c=grayMatrix[j])
    #ax.scatter(X, Y, s=20.0 * m[0], c=m[0], cmap='gist_yarg')
    ax.contourf(X, Y, m[0])
    
    #setPipe(); 
    setInVelocity()
    setObstacle(0.2, 0.50, 0.15)

overRelaxation = 1.9; dt = 1.0/60.0; density = 1000.0; nX = 300; nY = 300; 
res = 100.0; domainHeight = 1.0; domainWidth = domainHeight / nX*nY; h = domainHeight / res
cp = density*h/dt; gravity = 0.0; #-9.81; 
nX = math.floor(domainWidth/h); nY = math.floor(domainHeight/h); numCells = nX * nY

xAxis = np.arange(0, nX, 1); yAxis = np.arange(0, nY, 1); grid = np.zeros([nX, nY])
pressureColor = np.zeros([nX, nY, 4])
u = np.zeros([2, nX, nY]); v = np.zeros_like(u); m = np.zeros_like(u); m[0] = 1.0
p = np.zeros_like(grid); s = np.zeros_like(grid)

setObstacle(0.2, 0.50, 0.15); setPipe(); setInVelocity()

X, Y = np.meshgrid(xAxis, yAxis); nFrames = 200
fig, ax = mplt.subplots(1); fig.tight_layout(pad=0); fig.set_facecolor('black')
anim = FuncAnimation(fig, func=animFunc, frames=np.linspace(0, nFrames, num=nFrames), interval=1)
anim.save("waterSimPressureT6.gif")
#mplt.show()