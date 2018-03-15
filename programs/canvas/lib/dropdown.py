from pygame import font, Surface, Rect, Color
font.init()
dropdownFont = font.Font('fonts/Lato-Regular.ttf',16)
class Dropdown:
    def __init__(self, position: tuple, width: tuple = None, height: int = 26, label: str = "Unnamed", normalColour: Color = (225, 225, 225),
                 hoverColour: Color = (190, 190, 190),
                 clickColour: Color = (170, 170, 170)):
        self.position = position
        self.width = width
        self.height = height
        self.label = label
        self.buttons = []
        self.open = False
        self.normalColour = normalColour
        self.hoverColour = hoverColour
        self.clickColour = clickColour
        self.lastButtonState = [False, False, False]
    def draw(self,surface, mousePos, mouseButtons):
        drawSurf = Surface((self.getWidth(), self.height))
        if self.getRect().collidepoint(mousePos) or self.open:
            if mouseButtons[0] or self.open:
                drawSurf.fill(self.clickColour)
            else:
                drawSurf.fill(self.hoverColour)
        else:
            drawSurf.fill(self.normalColour)
        dropdownLabel = dropdownFont.render(self.label, True, (60, 60, 60))
        drawSurf.blit(dropdownLabel, (drawSurf.get_width()//2-dropdownLabel.get_width()//2, drawSurf.get_height()//2-dropdownLabel.get_height()//2))
        surface.blit(drawSurf,self.position)
        if self.open:
            widestButton = self.findWidestButton()
            for i,v in enumerate(self.buttons):
                surface.blit(v.draw(mousePos, mouseButtons, self.position[0], self.position[1]+self.height+i*v.height, widestButton),(self.position[0], self.position[1]+self.height+i*v.height))
    def update(self, mousePos, mouseButtons):
        if self.open:
            widestButton = self.findWidestButton()
            for i,v in enumerate(self.buttons):
                v.update(mousePos, mouseButtons, self.position[0], self.position[1]+self.height+i*v.height, widestButton)
        if self.getRect().collidepoint(mousePos) and mouseButtons[0] and not self.lastButtonState[0]:
            self.open = not self.open
        elif mouseButtons[0] and not self.lastButtonState[0]:
            self.open = False
        self.lastButtonState = mouseButtons
    def getRect(self):
        return Rect(self.position[0], self.position[1], self.getWidth(), self.height)
    def getWidth(self):
        if self.width == None:
            return dropdownFont.size(self.label)[0]+10
        else:
            return self.width
    def addButton(self, button):
        self.buttons.append(button)
    def findWidestButton(self):
        widest = 0
        for i in self.buttons:
            widest = max(widest, i.getWidth())
        return widest