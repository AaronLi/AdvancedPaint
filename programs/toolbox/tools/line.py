from pygame import draw
from math import hypot
import programs.toolbox.tools.tool as tool
class Line(tool.Tool):
    def drawFunc(self):
        distX = self.mPos[0] - self.oMPos[0]
        distY = self.mPos[1] - self.oMPos[1]
        totalDistance = max(hypot(distX, distY), 1)
        incX = distX / totalDistance
        incY = distY / totalDistance
        for i in range(int(totalDistance)):
            draw.circle(self.surface, self.colour,
                        (int(incX * totalDistance + self.oMPos[0]), int(incY * totalDistance + self.oMPos[1])),
                        self.radius,
                        self.fill_amount)
    def update(self): # only updates oMPos when mouse is initially clicked and while the mouse isn't pressed
        if self.tool_enabled and self.mButtons[0]:
            self.drawFunc()
        if self.mouseJustClicked():
            self.oMPos = self.mPos
        elif not self.mButtons[0]:
            self.oMPos = self.mPos
        self.oMButtons = self.mButtons