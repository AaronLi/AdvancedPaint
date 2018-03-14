from pygame import Rect, draw, font, image
import lib.cursor, lib.window, lib.tools
font.init()
minimizedWindowFont = font.Font("fonts/Lato-Regular.ttf",17)

arrow_cursor = lib.cursor.Cursor(image.load('img/cursors/arrow_cursor.png').convert_alpha())
arrow_move = lib.cursor.Cursor(image.load('img/cursors/arrow_move.png').convert_alpha(),True, True)
arrow_news = lib.cursor.Cursor(image.load('img/cursors/arrow_news.png').convert_alpha(), True, True)
arrow_ns = lib.cursor.Cursor(image.load('img/cursors/arrow_ns.png').convert_alpha(), True, True)
arrow_nwes = lib.cursor.Cursor(image.load('img/cursors/arrow_nwes.png').convert_alpha(), True, True)
arrow_we = lib.cursor.Cursor(image.load('img/cursors/arrow_we.png').convert_alpha(), True, True)

class DeskEnv:
    def __init__(self, size):
        self.windows = []
        self.size = size
        self.lastButtonState = (False, False, False)
        self.currentCursor = arrow_cursor
    def update(self, mousePos, buttonPress):
        minimizedWindows = []
        for i in range(len(self.windows)-1,-1,-1):
            windowPos = self.windows[i].position
            windowSize = self.windows[i].windowCanvas.get_size()
            if buttonPress[0] and Rect(windowPos,windowSize).collidepoint(mousePos) and not self.lastButtonState[0]:
                self.windows.append(self.windows.pop(i))
                break
        interactableWindow = True
        changedCursor = False
        for i in range(len(self.windows)-1,-1,-1):
            windowResize, windowDrag, resizeHover = self.windows[i].update(mousePos, buttonPress, Rect(0, 0, self.size[0], self.size[1] - 40),i==len(self.windows)-1, interactableWindow)
            if any(windowResize) or windowDrag:
                interactableWindow = False
            if self.windows[i].minimized and not self.windows[i].closed:
                minimizedWindows.append(self.windows[i])
                del self.windows[i]
            if resizeHover[lib.window.Window.WINDOW_TOP] or resizeHover[lib.window.Window.WINDOW_BOTTOM]:
                self.currentCursor = arrow_ns
                changedCursor = True
            elif resizeHover[lib.window.Window.WINDOW_LEFT] or resizeHover[lib.window.Window.WINDOW_RIGHT]:
                self.currentCursor = arrow_we
                changedCursor = True
            if not changedCursor:
                self.currentCursor = arrow_cursor
        for i in range(len(self.windows) - 1, -1, -1):
            if self.windows[i].closed and not self.lastButtonState[0] and buttonPress[0]:
                del self.windows[i]
                break
        for i, v in enumerate(minimizedWindows):
            if Rect(i * 201, self.size[1] - 40, 200, 40).collidepoint(mousePos) and buttonPress[0] and not \
            self.lastButtonState[0]:
                v.unMinimize()
                self.windows.append(minimizedWindows.pop(i))
        self.windows = list(reversed(minimizedWindows))+self.windows
        self.lastButtonState = buttonPress

    def draw(self, surface, mousePos, buttonPress):
        minimizedWindows = []
        for i,v in enumerate(self.windows):
            v.draw(surface, mousePos, buttonPress, i==len(self.windows)-1, Rect(0, 0, self.size[0], self.size[1] - 40))
            if v.minimized:
                minimizedWindows.append(v)
        draw.rect(surface, (240, 240, 240), (0, self.size[1] - 40, self.size[0], 40))
        for i, v in enumerate(reversed(minimizedWindows)):
            windowBarRect = Rect(i * 201, self.size[1] - 40, 200, 40)
            if windowBarRect.collidepoint(mousePos):
                draw.rect(surface, (190, 190, 190), windowBarRect)
            else:
                draw.rect(surface, (200, 200, 200), windowBarRect)
            minimizedLabel = minimizedWindowFont.render(lib.tools.clipText(v.windowTitle,194, minimizedWindowFont),True,(255,255,255))
            surface.blit(minimizedLabel,(i*201+3, self.size[1]-20-minimizedLabel.get_height()//2))
        self.currentCursor.draw(surface, mousePos, 0.6)
    def addWindow(self, window):
        self.windows.append(window)

    def resize(self, newSize):
        self.size = newSize
        for i in self.windows:
            if i.maximized:
                i.unMaximize()
                i.maximize(Rect(0, 0, self.size[0], self.size[1] - 40))
