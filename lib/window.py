from pygame import Surface, draw, Rect, font

font.init()
lato = font.Font("fonts/Lato-Regular.ttf", 15)


class Window:
    def __init__(self, windowTitle="Empty Window", xPos=10, yPos=10, width=800, height=620):
        self.windowTitle = windowTitle
        self.position = [xPos, yPos]
        self.windowCanvas = Surface((width, height))
        self.closeButtonRect = Rect(width - 61, 0, 60, 20)
        self.growButtonRect = Rect(width - 122, 0, 60, 20)
        self.minimizeButtonRect = Rect(width - 183, 0, 60, 20)
        self.lastButtonState = [False, False, False]
        self.difX, self.difY = 0, 0
        self.minimized = False
        self.maximized = False
        self.closed = False
        self.previousSize = width, height
        self.previousPos = self.position
    def draw(self, surface: Surface, mousePos, mouseButtons):
        mousePos = (mousePos[0] - self.position[0], mousePos[1] - self.position[1])

        self.windowCanvas.fill((0, 0, 0))
        draw.rect(self.windowCanvas, (240, 240, 240), (0, 0, self.getWindowWidth(), 20))
        draw.rect(self.windowCanvas, (240, 240, 240), (0, 0, self.getWindowWidth(), self.getWindowHeight()),4)

        windowTitleRender = lato.render(self.windowTitle, True, (180, 180, 180))
        self.windowCanvas.blit(windowTitleRender, (2, 0))

        if self.closeButtonRect.collidepoint(mousePos):
            if mouseButtons[0]:
                draw.rect(self.windowCanvas, (200, 0, 0), self.closeButtonRect)
            else:
                draw.rect(self.windowCanvas, (255, 0, 0), self.closeButtonRect)
        else:
            draw.rect(self.windowCanvas, (220, 220, 220), self.closeButtonRect)
        if self.growButtonRect.collidepoint(mousePos):
            if mouseButtons[0]:
                draw.rect(self.windowCanvas, (190, 190, 190), self.growButtonRect)
            else:
                draw.rect(self.windowCanvas, (200, 200, 200), self.growButtonRect)
        else:
            draw.rect(self.windowCanvas, (220, 220, 220), self.growButtonRect)
        if self.minimizeButtonRect.collidepoint(mousePos):
            if mouseButtons[0]:
                draw.rect(self.windowCanvas, (190, 190, 190), self.minimizeButtonRect)
            else:
                draw.rect(self.windowCanvas, (200, 200, 200), self.minimizeButtonRect)
        else:
            draw.rect(self.windowCanvas, (220, 220, 220), self.minimizeButtonRect)

        if not self.minimized:
            surface.blit(self.windowCanvas, self.position)

    def update(self, mousePos: tuple, mouseButtons: tuple, availableSpace : Rect):
        canvasMousePos = (mousePos[0] - self.position[0], mousePos[1] - self.position[1])
        if not self.minimized:
            if Rect(self.position + list(self.getControlBarSize())).collidepoint(mousePos) and mouseButtons[0]:
                if not self.lastButtonState[0] and mouseButtons[0]:
                    self.difX = self.position[0] - mousePos[0]
                    self.difY = self.position[1] - mousePos[1]
                self.position = [mousePos[0] + self.difX, mousePos[1] + self.difY]
                if self.maximized:
                    self.unMaximize()
                    self.position = [0,0]
                    self.resize(availableSpace.size)
            if self.minimizeButtonRect.collidepoint(canvasMousePos) and mouseButtons[0]:
                self.minimize()
            elif self.growButtonRect.collidepoint(canvasMousePos) and mouseButtons[0]:
                if self.maximized:
                    self.unMaximize()
                else:
                    self.maximize(availableSpace)
            elif self.closeButtonRect.collidepoint(canvasMousePos) and mouseButtons[0]:
                self.close()
        self.lastButtonState = mouseButtons
    def minimize(self):
        self.minimized = True
    def unMinimize(self):
        self.minimized = False
    def maximize(self,availableSpace :Rect):
        self.previousPos = self.position
        self.previousSize = (self.getWindowWidth(), self.getWindowHeight())
        self.position = list(availableSpace.topleft)
        self.resize(availableSpace.size)
        self.maximized = True
    def unMaximize(self):
        self.position = self.previousPos
        self.resize(self.previousSize)
        self.maximized = False
    def resize(self,newSize):
        self.windowCanvas = Surface(newSize)
        self.closeButtonRect = Rect(self.getWindowWidth() - 61, 0, 60, 20)
        self.growButtonRect = Rect(self.getWindowWidth() - 122, 0, 60, 20)
        self.minimizeButtonRect = Rect(self.getWindowWidth() - 183, 0, 60, 20)
    def close(self):
        self.closed = True
    def getWindowWidth(self):
        return self.windowCanvas.get_width()

    def getWindowHeight(self):
        return self.windowCanvas.get_height()

    def getDrawWidth(self):
        return self.getWindowWidth()

    def getDrawHeight(self):
        return self.getWindowHeight() - 20

    def getControlBarSize(self):
        return self.getWindowWidth(), 20
    def collideWindow(self, point):
        return Rect(self.position,self.windowCanvas.get_size()).collidepoint(point)