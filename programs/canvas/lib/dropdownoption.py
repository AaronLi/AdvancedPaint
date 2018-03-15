from pygame import font, Surface, Color, Rect
font.init()
dropDownOptionFont = font.Font('fonts/Lato-Regular.ttf',14)
class DropDownOption:
    def __init__(self, label = "Unnammed", height = 30, function= None, normalColour: Color = (210, 210, 210),
                 hoverColour: Color = (190, 190, 190),
                 clickColour: Color = (180, 180, 180)):
        self.label = label
        self.height = height
        self.function = function
        self.normalColour = normalColour
        self.hoverColour = hoverColour
        self.clickColour = clickColour
        self.previousButtonStates = [False, False, False]
    def update(self, mousePos, mouseButtons, xPos, yPos, width = None):
        if width == None:
            clickArea = Rect(xPos, yPos, self.getWidth(), self.height)
        else:
            clickArea = Rect(xPos, yPos, width, self.height)
        if clickArea.collidepoint(mousePos) and mouseButtons[0] and not self.previousButtonStates[0]:
            if self.function!=None:
                self.function()
            else:
                print('Dropdown option: "%s" clicked'%self.label)
        self.previousButtonStates = mouseButtons
    def draw(self, mousePos, mouseButtons, xPos, yPos, width = None):
        if width == None:
            drawSurf = Surface((self.getWidth(), self.height))
        else:
            drawSurf = Surface((width, self.height))
        if Rect(xPos, yPos, drawSurf.get_width(), drawSurf.get_height()).collidepoint(mousePos):
            if mouseButtons[0]:
                drawSurf.fill(self.clickColour)
            else:
                drawSurf.fill(self.hoverColour)
        else:
            drawSurf.fill(self.normalColour)
        renderedLabel = dropDownOptionFont.render(self.label, True, (60, 60, 60))
        drawSurf.blit(renderedLabel,(13, drawSurf.get_height()//2-renderedLabel.get_height()//2))
        return drawSurf
    def getWidth(self):
        return dropDownOptionFont.size(self.label)[0]+60
