import programs.toolbox.tools.tool as tool
from pygame import draw
from math import hypot
class Pen(tool.Tool):
    def drawFunc(self):
        distX = self.mPos[0] - self.oMPos[0]
        distY = self.mPos[1] - self.oMPos[1]
        totalDistance = max(hypot(distX, distY), 1)
        incX = distX / totalDistance
        incY = distY / totalDistance
        for i in range(int(totalDistance)):
            draw.circle(self.surface, self.colour, (int(incX * totalDistance + self.oMPos[0]), int(incY * totalDistance + self.oMPos[1])), self.radius,
                        self.fill_amount)