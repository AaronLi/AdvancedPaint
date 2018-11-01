from pygame import Surface, draw, Rect, font, image
import traceback, sys
import lib.mathTools, lib.windowedprogram

font.init()
lato = font.Font("fonts/Lato-Regular.ttf", 15)

close_icon = image.load('img/windowIcons/close_icon.png').convert_alpha()
maximize_icon = image.load('img/windowIcons/maximize_icon.png').convert_alpha()
minimize_icon = image.load('img/windowIcons/minimize_icon.png').convert_alpha()
unmaximize_icon = image.load('img/windowIcons/unmaximize_icon.png').convert_alpha()
maximize_icon_disabled = image.load('img/windowIcons/maximize_icon_greyed_out.png').convert_alpha()
unmaximize_icon_disabled = image.load('img/windowIcons/unmaximize_icon_greyed_out.png').convert_alpha()

class Window:
    WINDOW_TOP = 0
    WINDOW_LEFT = 1
    WINDOW_RIGHT = 2
    WINDOW_BOTTOM = 3

    def __init__(self, xPos=10, yPos=10, width=800, height=620, program=lib.windowedprogram.WindowedProgram, programParameters = None):
        self.windowTitle = ""
        self.position = [xPos, yPos]
        self.windowCanvas = Surface((width, height))
        self.closeButtonRect = Rect(width - 61, 0, 60, 20)
        self.growButtonRect = Rect(width - 122, 0, 60, 20)
        self.minimizeButtonRect = Rect(width - 183, 0, 60, 20)
        self.lastButtonState = [False, False, False]
        self.minimized = False
        self.maximized = False
        self.closed = False
        self.beingResized = [False, False, False, False]
        self.beingDragged = False
        self.snap = [False, False, False]
        self.previousSize = width, height
        self.previousPos = self.position
        self.crashed = False
        self.resizable = True
        self.program = program(self.getDrawArea(), self, programParameters)
        self.program.configure()
        self.drag_offset_x, self.drag_offset_y = 0, 0

    def draw(self, surface: Surface, mousePos, mouseButtons, focused, availableSpace):
        normalisedMousePos = (mousePos[0] - self.position[0], mousePos[1] - self.position[1])

        self.windowCanvas.fill((0, 0, 0))
        try:
            self.windowCanvas.blit(self.program.draw(self.programMousePos(mousePos), mouseButtons), (3, 20))
        except:
            self.crash("Program %s crashed during draw call..." % self.program.name)
        if focused:
            draw.rect(self.windowCanvas, (240, 240, 240), (0, 0, self.getWindowWidth(), 20))
            draw.rect(self.windowCanvas, (240, 240, 240), (0, 0, self.getWindowWidth(), self.getWindowHeight()), 4)
        else:
            draw.rect(self.windowCanvas, (250, 250, 250), (0, 0, self.getWindowWidth(), 20))
            draw.rect(self.windowCanvas, (250, 250, 250), (0, 0, self.getWindowWidth(), self.getWindowHeight()), 4)
        windowTitleRender = lato.render(lib.mathTools.clipText(self.windowTitle, self.getWindowWidth() - 185, lato), True,
                                        (60, 60, 60) if focused else (200, 200, 200))
        self.windowCanvas.blit(windowTitleRender, (2, 0))
        if self.closeButtonRect.collidepoint(normalisedMousePos):
            if mouseButtons[0]:
                draw.rect(self.windowCanvas, (200, 0, 0), self.closeButtonRect)
            else:
                draw.rect(self.windowCanvas, (255, 0, 0), self.closeButtonRect)
        else:
            draw.rect(self.windowCanvas, (220, 220, 220), self.closeButtonRect)
        if not self.resizable:
            draw.rect(self.windowCanvas, (235, 235, 235), self.growButtonRect)
        elif self.growButtonRect.collidepoint(normalisedMousePos):
            if mouseButtons[0]:
                draw.rect(self.windowCanvas, (190, 190, 190), self.growButtonRect)
            else:
                draw.rect(self.windowCanvas, (200, 200, 200), self.growButtonRect)
        else:
            draw.rect(self.windowCanvas, (220, 220, 220), self.growButtonRect)
        if self.minimizeButtonRect.collidepoint(normalisedMousePos):
            if mouseButtons[0]:
                draw.rect(self.windowCanvas, (190, 190, 190), self.minimizeButtonRect)
            else:
                draw.rect(self.windowCanvas, (200, 200, 200), self.minimizeButtonRect)
        else:
            draw.rect(self.windowCanvas, (220, 220, 220), self.minimizeButtonRect)
        self.windowCanvas.blit(minimize_icon, (
        self.minimizeButtonRect.x - minimize_icon.get_width() // 2 + self.minimizeButtonRect.width // 2,
        self.minimizeButtonRect.y - minimize_icon.get_height() // 2 + self.growButtonRect.height // 2))
        if self.maximized:
            self.windowCanvas.blit(unmaximize_icon if self.resizable else unmaximize_icon_disabled, (
            self.growButtonRect.x - unmaximize_icon.get_width() // 2 + self.growButtonRect.width // 2,
            self.growButtonRect.y - unmaximize_icon.get_height() // 2 + self.growButtonRect.height // 2))
        else:
            self.windowCanvas.blit(maximize_icon if self.resizable else maximize_icon_disabled , (
            self.growButtonRect.x - maximize_icon.get_width() // 2 + self.growButtonRect.width // 2,
            self.growButtonRect.y - maximize_icon.get_height() // 2 + self.growButtonRect.height // 2))
        self.windowCanvas.blit(close_icon,
                               (self.closeButtonRect.x - close_icon.get_width() // 2 + self.growButtonRect.width // 2,
                                self.closeButtonRect.y - close_icon.get_height() // 2 + self.growButtonRect.height // 2))
        if not self.minimized:
            surface.blit(self.windowCanvas, self.position)
            if self.snap[Window.WINDOW_TOP]:
                draw.rect(surface, (200, 200, 200), availableSpace, 2)
            elif self.snap[Window.WINDOW_LEFT]:
                draw.rect(surface, (200, 200, 200),
                          availableSpace.inflate(availableSpace.width // -2, 0).move(availableSpace.width // -4, 0), 2)
            elif self.snap[Window.WINDOW_RIGHT]:
                draw.rect(surface, (200, 200, 200),
                          availableSpace.inflate(availableSpace.width // -2, 0).move(availableSpace.width // 4, 0), 2)

    def update(self, mousePos: tuple, mouseButtons: tuple, availableSpace: Rect, focused: bool, interactable=True):
        resizeReady = [False, False, False, False]
        canvasMousePos = (mousePos[0] - self.position[0], mousePos[1] - self.position[1])
        if mouseButtons[0]:
            if self.beingDragged:
                self.position = [mousePos[0] - self.drag_offset_x, mousePos[1] - self.drag_offset_y]
            elif not self.minimized and interactable:
                # Dragging logic and snapping logic
                if self.get_title_bar_rect().collidepoint(mousePos) and not self.beingDragged and focused and not any(self.beingResized):

                    #the window can be dragged if the mouse is touching the title bar, if it's not already being dragged, if it's focused, and if it's not being resized

                    self.set_being_dragged(mouseButtons[0], mousePos)
                    if self.resizable:
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
                        self.position = [availableSpace.width // 2, 0]
                        self.snap[Window.WINDOW_RIGHT] = False
                if focused and self.resizable:
                    if not any(self.beingResized):
                        for index, side in enumerate(self.get_hot_edges()):
                            if side.collidepoint(mousePos):
                                self.set_being_resized(True, index)
                                break
                    else:
                        for index, being_resized in enumerate(self.beingResized):
                            if being_resized == True:
                                self.resize_to_mouse(mousePos, index)
                # Window control buttons
                if self.minimizeButtonRect.collidepoint(canvasMousePos) and mouseButtons[0] and not self.lastButtonState[0]:
                    self.minimize()
                elif self.growButtonRect.collidepoint(canvasMousePos) and mouseButtons[0] and not self.lastButtonState[0] and self.resizable:
                    if self.maximized:
                        self.unMaximize()
                    else:
                        self.maximize(availableSpace)
                elif self.closeButtonRect.collidepoint(canvasMousePos) and mouseButtons[0] and not self.lastButtonState[0]:
                    self.close()
        else:
            self.set_being_dragged(False)
            self.set_being_resized(False)
        if focused and not self.minimized:
            try:
                self.program.update(self.programMousePos(mousePos), mouseButtons)
            except:
                self.crash("Program %s crashed during update call..." % self.program.name)
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
        newSize = [max(newSize[0], self.closeButtonRect.right - self.minimizeButtonRect.left +4), max(newSize[1], 25)]
        print("Window: \"%s\" resized to (%d, %d)" % (self.windowTitle, newSize[0], newSize[1]))
        self.windowCanvas = Surface(newSize)
        self.closeButtonRect = Rect(self.getWindowWidth() - 61, 0, 60, 20)
        self.growButtonRect = Rect(self.getWindowWidth() - 122, 0, 60, 20)
        self.minimizeButtonRect = Rect(self.getWindowWidth() - 183, 0, 60, 20)
        try:
            self.program.resize(self.getDrawArea())
        except:
            self.crash("Program %s crashed during resize call..." % self.program.name)

    def close(self):
        print("Window: \"%s\" closed" % self.windowTitle)
        self.closed = True

    def crash(self, message=""):
        sys.stderr.write("\n" + "-" * 44 + "Message" + "-" * 44 + "\n")
        sys.stderr.write(message + "\n")
        sys.stderr.write("-" * 40 + "Stack Traceback" + "-" * 40 + "\n")
        traceback.print_exc()
        sys.stderr.write("\n")
        self.crashed = True

    def programMousePos(self, mousePos):
        return (mousePos[0] - self.position[0] - 3, mousePos[1] - self.position[1] - 20)
    def scaleToDrawArea(self, area):
        self.resize((area[0]+5,area[1]+22))
        return self.getDrawArea()
    def getDrawArea(self):
        return self.getDrawWidth(), self.getDrawHeight()

    def getWindowWidth(self):
        return self.windowCanvas.get_width()

    def getWindowHeight(self):
        return self.windowCanvas.get_height()

    def getDrawWidth(self):
        return self.getWindowWidth() - 5

    def getDrawHeight(self):
        return self.getWindowHeight() - 22

    def getRight(self):
        return self.position[0] + self.getWindowWidth()

    def getBottom(self):
        return self.position[1] + self.getWindowHeight()

    def getControlBarSize(self):
        return self.getWindowWidth(), 20

    def collideWindow(self, point):
        return Rect(self.position, self.windowCanvas.get_size()).collidepoint(point)

    def get_usable_title_bar_space(self):
        #the amount of space that remains after the buttons are filled in
        return self.getWindowWidth() - self.minimizeButtonRect.left

    def set_being_dragged(self, state :bool, mousePos = (0, 0)):
        if state == True:
            self.drag_offset_x = mousePos[0] - self.position[0]
            self.drag_offset_y = mousePos[1] - self.position[1]
            self.beingDragged = True
        else:
            self.beingDragged = False

    def set_being_resized(self, state :bool, side = -1):
        if state == True:
            if side > -1:
                self.beingResized[side] = state
            else:
                raise ValueError("Invalid side %d"%side)
        else:
            for i in range(len(self.beingResized)):
                self.beingResized[i] = False

    def get_title_bar_rect(self):
        #the box is moved 4 pixels down to make space for the dragging area
        #the box is shrunk 183 pixels in width to make space for the close, minimize, and expand buttons
        return Rect(self.position[0], self.position[1] + 4, self.getWindowWidth(), 16)

    def get_hot_edges(self):
        title_bar_rect = self.get_title_bar_rect()
        return [
            Rect(self.position[0], self.position[1]-10, self.get_usable_title_bar_space(), 14), #top
            Rect(self.position[0]-4, title_bar_rect.bottom, 7, self.getWindowHeight()-(title_bar_rect.bottom - self.position[1])), #left
            Rect(self.position[0] + self.getWindowWidth() -3, title_bar_rect.bottom, 7, self.getWindowHeight() - (title_bar_rect.bottom - self.position[1])), #right
            Rect(self.position[0], self.getWindowHeight()-3, self.getWindowWidth(), 7) #bottom
        ]

    def resize_to_mouse(self, mousePos :tuple, side :int):

        if side == Window.WINDOW_TOP:
            self.resize((self.getWindowWidth(), self.getBottom()-mousePos[1]))
            self.position = [self.position[0], mousePos[1]]

        elif side == Window.WINDOW_LEFT:
            self.resize((self.getRight() - mousePos[0], self.getWindowHeight()))
            self.position = [mousePos[0], self.position[1]]

        elif side == Window.WINDOW_RIGHT:
            self.resize((mousePos[0] - self.position[0], self.getWindowHeight()))
            self.position = self.position #unchanged

        elif side == Window.WINDOW_BOTTOM:
            self.resize((self.getWindowWidth(), mousePos[1] - self.position[1]))
            self.position = self.position #unchanged

    def get_window_buttons_rect(self):
        return Rect(self.minimizeButtonRect.left, self.minimizeButtonRect.top, self.closeButtonRect.right - self.minimizeButtonRect.left, self.minimizeButtonRect.height)