import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

class Star():
  global width, height

  def __init__(self):
    self.x = 2.0 * np.random.rand() - 1.0
    self.y = 2.0 * np.random.rand() - 1.0
    self.z = np.random.rand()
    self.sx = 0.0; self.sy = 0.0; self.size = 0.0; self.pz = 0.0; self.tx = 0.0; self.ty = 0.0

  def update(self):
    self.z = self.z - 0.1
    if(self.z < 0.0):
      self.z = 1.0
      self.x = 2.0 * np.random.rand() - 1.0
      self.y = 2.0 * np.random.rand() - 1.0

  def show(self):
    self.sx = self.x/self.z
    self.sy = self.y/self.z
    self.size = normalizeScalar(self.z, 0.0, 1.0, 46.0, 0.0 )
    return self.sx, self.sy, self.size

  def showTrail(self):
    self.tx = (self.sx / 1.951)
    self.ty = (self.sy / 1.951)
    return [self.tx, self.sx], [self.ty, self.sy]

def normalizeVector(values, lowerDes, upperDes, lowerAct, upperAct):
  return [lowerDes + (x - lowerAct) * (upperDes - lowerDes) / (upperAct - lowerAct) for x in values]

def normalizeScalar(value, lowerAct, upperAct, lowerDes, upperDes):
  return lowerDes + (value - lowerAct) * (upperDes - lowerDes) / (upperAct - lowerAct)

def pincushionTransform(xV, yX):
  rsq = xV**2.0 + yX**2.0 + np.ones_like(xV)*0.04
  rX = xV * rsq; rY = yX * rsq
  return rX, rY

def hyperbolicTransform(hX, hY):
  xA = hX*(1.0 - (hY**2.0)*0.5)**0.5; yA = hY*(1.0 - (hX**2.0)*0.5)**0.5
  return xA, yA

def animationFunc(i):
  global stars, coordinateArray, sizeArray, rateArray

  #if(angleOfRotation.max() <= 1.0):
  #  ax.elev = 90 * lerp
  #  angleOfRotation = angleOfRotation + rate
  #  cosScalar = np.cos(angleOfRotation); sinScalar = np.sin(angleOfRotation)
  #else:
  #  rate = np.ones_like(X) * 0.006
  #  angleOfRotation = angleOfRotation + rate
  #  cosScalar = np.cos(angleOfRotation); sinScalar = np.sin(angleOfRotation)

  ax1.clear(); ax1.axis('off'); ax1.set_xlim([-1.0, 1.0]); ax1.set_ylim([-1.0, 1.0])
  for j in range(len(stars)):
    coordinateArray[0][j], coordinateArray[1][j], sizeArray[0][j] = stars[j].show()

    trailArrayX[j], trailArrayY[j] = stars[j].showTrail()
    #ax1.plot(trailArrayX[j], trailArrayY[j], color='w', linewidth=0.50)
    pTX, pTY = pincushionTransform(trailArrayX[j], trailArrayY[j]); ax1.plot(pTX, pTY, color='w', linewidth=0.50)

    stars[j].update()

  pX, pY = pincushionTransform(coordinateArray[0], coordinateArray[1]); ax1.scatter(pX, pY, s=sizeArray, color='w')
  #ax1.scatter(coordinateArray[0], coordinateArray[1], s=sizeArray, color='w');

height = 100; width = 100; step = 1
xAxis = np.arange(-width, width + step, step); yAxis = np.arange(-height, height + step, step); X,Y = np.meshgrid(xAxis, yAxis)
angleOfRotation = np.zeros_like(X); rate = np.zeros_like(X); rateInc = 0.09
for i in range(rate.shape[0]):
    for y in range(rate.shape[1]):
        rate[i][y] = rateInc
        rate[y][i] = rateInc
        rate[rate.shape[0] - 1 - i][rate.shape[1] - 1 - y] = rateInc
        rate[rate.shape[1] - 1 - y][rate.shape[0] - 1 - i] = rateInc
    rateInc *= 0.8

stars = []; totalNumStars = 75
for i in range(totalNumStars):
  stars.append(Star())
coordinateArray = np.zeros([2, len(stars)]); trailArrayX = np.zeros([len(stars), 2]); trailArrayY = np.zeros([len(stars), 2]);
sizeArray = np.zeros([1, len(stars)])

fig, ax1 = mplt.subplots(1, facecolor="black", dpi=100)
fig.tight_layout(pad=0); ax1.axis('off')
anim = FuncAnimation(fig, func=animationFunc, frames=np.linspace(0, 50, num=50), interval=1)
anim.save('starField_T1.gif')
mplt.show()