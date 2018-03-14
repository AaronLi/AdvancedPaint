from pygame import Surface, draw, Rect, font, image
import lib.tools
font.init()
lato = font.Font("fonts/Lato-Regular.ttf", 15)

close_icon = image.load('img/windowIcons/close_icon.png').convert_alpha()
maximize_icon = image.load('img/windowIcons/maximize_icon.png').convert_alpha()
minimize_icon = image.load('img/windowIcons/minimize_icon.png').convert_alpha()
unmaximize_icon = image.load('img/windowIcons/unmaximize_icon.png').convert_alpha()

class Window:
    WINDOW_TOP = 0
    WINDOW_LEFT = 1
    WINDOW_RIGHT = 2
    WINDOW_BOTTOM = 3

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
        self.beingResized = [False, False, False, False]
        self.beingDragged = False
        self.snap = [False, False, False]
        self.previousSize = width, height
        self.previousPos = self.position

    def draw(self, surface: Surface, mousePos, mouseButtons, focused, availableSpace):
        mousePos = (mousePos[0] - self.position[0], mousePos[1] - self.position[1])

        self.windowCanvas.fill((0, 0, 0))
        if focused:
            draw.rect(self.windowCanvas, (240, 240, 240), (0, 0, self.getWindowWidth(), 20))
            draw.rect(self.windowCanvas, (240, 240, 240), (0, 0, self.getWindowWidth(), self.getWindowHeight()), 4)
        else:
            draw.rect(self.windowCanvas, (250, 250, 250), (0, 0, self.getWindowWidth(), 20))
            draw.rect(self.windowCanvas, (250, 250, 250), (0, 0, self.getWindowWidth(), self.getWindowHeight()), 4)
        windowTitleRender = lato.render(lib.tools.clipText(self.windowTitle,self.getWindowWidth()-185, lato), True, (60, 60, 60) if focused else (200, 200, 200))
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
        self.windowCanvas.blit(minimize_icon,(self.minimizeButtonRect.x-minimize_icon.get_width()//2+self.minimizeButtonRect.width//2, self.minimizeButtonRect.y-minimize_icon.get_height()//2 + self.growButtonRect.height//2))
        if self.maximized:
            self.windowCanvas.blit(unmaximize_icon, (self.growButtonRect.x - unmaximize_icon.get_width() // 2 +self.growButtonRect.width//2,
                                               self.growButtonRect.y - unmaximize_icon.get_height() // 2 + self.growButtonRect.height//2))
        else:
            self.windowCanvas.blit(maximize_icon, (self.growButtonRect.x - maximize_icon.get_width() // 2 +self.growButtonRect.width//2,
                                                   self.growButtonRect.y - maximize_icon.get_height() // 2 + self.growButtonRect.height//2))
        self.windowCanvas.blit(close_icon, (self.closeButtonRect.x - close_icon.get_width() // 2 + self.growButtonRect.width // 2,
                                               self.closeButtonRect.y - close_icon.get_height() // 2 + self.growButtonRect.height//2))
        if not self.minimized:
            surface.blit(self.windowCanvas, self.position)
            if self.snap[Window.WINDOW_TOP]:
                draw.rect(surface, (200, 200, 200), availableSpace, 2)
            elif self.snap[Window.WINDOW_LEFT]:
                draw.rect(surface, (200, 200, 200), availableSpace.inflate(availableSpace.width//-2,0).move(availableSpace.width//-4,0), 2)
            elif self.snap[Window.WINDOW_RIGHT]:
                draw.rect(surface, (200, 200, 200), availableSpace.inflate(availableSpace.width//-2,0).move(availableSpace.width//4,0), 2)
    def update(self, mousePos: tuple, mouseButtons: tuple, availableSpace: Rect, focused: bool, interactable=True):
        resizeReady = [False, False, False, False]
        canvasMousePos = (mousePos[0] - self.position[0], mousePos[1] - self.position[1])
        if not self.minimized and interactable:
            # Dragging logic and snapping logic
            if ((Rect(self.position[0], self.position[1]+4, self.getWindowWidth() - 183, 16).collidepoint(
                    mousePos) and not self.beingDragged) or (
                Rect(self.position[0] - 100, self.position[1] - 100, self.getWindowWidth() - 133, 200).collidepoint(
                        mousePos) and self.beingDragged)) and mouseButtons[0] and focused and not any(self.beingResized):
                if not self.lastButtonState[0] and mouseButtons[0]:
                    self.difX = self.position[0] - mousePos[0]
                    self.difY = self.position[1] - mousePos[1]
                self.beingDragged = True
                if self.maximized:
                    self.unMaximize()
                elif mousePos[1] < availableSpace.top + 5:
                    self.snap[Window.WINDOW_TOP] = True

                elif mousePos[0] < availableSpace.left + 5:
                    self.snap[Window.WINDOW_LEFT] = True

                elif mousePos[0] > availableSpace.width - 5:
                    self.snap[Window.WINDOW_RIGHT] = True
                else:
                    self.snap = [False, False, False]
                self.position = [mousePos[0] + self.difX, mousePos[1] + self.difY]
            else:
                # Snap only occurs after dragging has stopped
                self.beingDragged = False
                if self.snap[Window.WINDOW_TOP] and self.lastButtonState[0] and not mouseButtons[0]:
                    self.maximize(availableSpace)
                    self.snap[Window.WINDOW_TOP] = False
                elif self.snap[Window.WINDOW_LEFT] and self.lastButtonState[0] and not mouseButtons[0]:
                    self.maximize(availableSpace.inflate(availableSpace.width // -2, 0))
                    self.position = [0, 0]
                    self.snap[Window.WINDOW_LEFT] = False
                elif self.snap[Window.WINDOW_RIGHT] and self.lastButtonState[0] and not mouseButtons[0]:
                    self.maximize(availableSpace.inflate(availableSpace.width // -2, 0))
                    self.position = [availableSpace.width//2, 0]
                    self.snap[Window.WINDOW_RIGHT] = False
            if ((canvasMousePos[0] in range(-4, 3) and not self.beingResized[Window.WINDOW_LEFT]) or (
                    canvasMousePos[0] in range(-9, 10) and self.beingResized[Window.WINDOW_LEFT])) and \
                            canvasMousePos[1] in range(20, self.getWindowHeight()):
                resizeReady[Window.WINDOW_LEFT] = True
                if mouseButtons[0]:
                    self.resize((self.getRight() - mousePos[0], self.getWindowHeight()))
                    self.position = [mousePos[0], self.position[1]]
                    self.beingResized[Window.WINDOW_LEFT] = True
            else:
                self.beingResized[Window.WINDOW_LEFT] = False
            if ((canvasMousePos[0] - self.getWindowWidth() in range(-4, 3) and not self.beingResized[
                Window.WINDOW_RIGHT]) or (
                        canvasMousePos[0] - self.getWindowWidth() in range(-12, 13) and self.beingResized[
                Window.WINDOW_RIGHT])) and canvasMousePos[1] in range(20, self.getWindowHeight()):
                resizeReady[Window.WINDOW_RIGHT] = True
                if mouseButtons[0]:
                    self.beingResized[Window.WINDOW_RIGHT] = True
                    self.resize((mousePos[0] - self.position[0], self.getWindowHeight()))
            else:
                self.beingResized[Window.WINDOW_RIGHT] = False
            if canvasMousePos[0] in range(3, self.getWindowWidth() - 2) and ((canvasMousePos[
                                                                                  1] - self.getWindowHeight() in range(
                    -10, 0) and not self.beingResized[Window.WINDOW_BOTTOM]) or (
                        canvasMousePos[1] - self.getWindowHeight() in range(-7, 8) and self.beingResized[
                Window.WINDOW_BOTTOM])):
                resizeReady[Window.WINDOW_BOTTOM] = True
                if mouseButtons[0]:
                    self.beingResized[Window.WINDOW_BOTTOM] = True
                    self.resize((self.getWindowWidth(), mousePos[1] - self.position[1]))
            else:
                self.beingResized[Window.WINDOW_BOTTOM] = False
            if canvasMousePos[0] in range(0, self.getWindowWidth()-183) and ((canvasMousePos[1] in range(-10,5) and not self.beingResized[Window.WINDOW_TOP]) or (canvasMousePos[1] in range(-15,13) and self.beingResized[Window.WINDOW_TOP])):
                resizeReady[Window.WINDOW_TOP] = True
                if mouseButtons[0]:
                    self.resize((self.getWindowWidth(), self.getBottom() - mousePos[1]))
                    self.position = [self.position[0], mousePos[1]]
                    self.beingResized[Window.WINDOW_TOP] = True
            else:
                self.beingResized[Window.WINDOW_TOP] = False
            # Window control buttons
            if self.minimizeButtonRect.collidepoint(canvasMousePos) and mouseButtons[0] and not self.lastButtonState[0]:
                self.minimize()
            elif self.growButtonRect.collidepoint(canvasMousePos) and mouseButtons[0] and not self.lastButtonState[0]:
                if self.maximized:
                    self.unMaximize()
                else:
                    self.maximize(availableSpace)
            elif self.closeButtonRect.collidepoint(canvasMousePos) and mouseButtons[0] and not self.lastButtonState[0]:
                self.close()
        self.lastButtonState = mouseButtons
        return self.beingResized, self.beingDragged, resizeReady

    def minimize(self):
        print("Window: \"%s\" minimized" % self.windowTitle)
        self.minimized = True

    def unMinimize(self):
        print("Window: \"%s\" unminimized" % self.windowTitle)
        self.minimized = False

    def maximize(self, availableSpace: Rect):
        self.previousPos = self.position
        self.previousSize = (self.getWindowWidth(), self.getWindowHeight())
        self.position = list(availableSpace.topleft)
        self.resize(availableSpace.size)
        self.maximized = True

    def unMaximize(self):
        self.position = self.previousPos
        self.resize(self.previousSize)
        self.maximized = False

    def resize(self, newSize):
        newSize = [max(newSize[0],185), max(newSize[1],25)]
        print("Window: \"%s\" resized to (%d, %d)" % (self.windowTitle, newSize[0], newSize[1]))
        self.windowCanvas = Surface(newSize)
        self.closeButtonRect = Rect(self.getWindowWidth() - 61, 0, 60, 20)
        self.growButtonRect = Rect(self.getWindowWidth() - 122, 0, 60, 20)
        self.minimizeButtonRect = Rect(self.getWindowWidth() - 183, 0, 60, 20)

    def close(self):
        print("Window: \"%s\" closed" % self.windowTitle)
        self.closed = True

    def getWindowWidth(self):
        return self.windowCanvas.get_width()

    def getWindowHeight(self):
        return self.windowCanvas.get_height()

    def getDrawWidth(self):
        return self.getWindowWidth()

    def getDrawHeight(self):
        return self.getWindowHeight() - 20

    def getRight(self):
        return self.position[0] + self.getWindowWidth()

    def getBottom(self):
        return self.position[1] + self.getWindowHeight()

    def getControlBarSize(self):
        return self.getWindowWidth(), 20

    def collideWindow(self, point):
        return Rect(self.position, self.windowCanvas.get_size()).collidepoint(point)
