from pygame import Rect, draw, font
font.init()
minimizedWindowFont = font.Font("fonts/Lato-Regular.ttf",20)

class DeskEnv:
    def __init__(self, size):
        self.windows = []
        self.size = size
        self.lastButtonState = (False, False, False)

    def update(self, mousePos, buttonPress):
        minimizedWindows = []
        for i in range(len(self.windows)-1,-1,-1):
            windowPos = self.windows[i].position
            windowSize = self.windows[i].windowCanvas.get_size()
            if buttonPress[0] and Rect(windowPos,windowSize).collidepoint(mousePos):
                self.windows.append(self.windows.pop(i))
                break
        for i,v in enumerate(self.windows):
            v.update(mousePos, buttonPress, Rect(0, 0, self.size[0], self.size[1] - 40),i==len(self.windows)-1)
            if v.minimized and not v.closed:
                minimizedWindows.append(v)
        for i in range(len(self.windows) - 1, -1, -1):
            if self.windows[i].closed:
                del self.windows[i]
        for i, v in enumerate(minimizedWindows):
            if Rect(i * 201, self.size[1] - 40, 200, 40).collidepoint(mousePos) and buttonPress[0] and not \
            self.lastButtonState[0]:
                v.unMinimize()
        self.lastButtonState = buttonPress

    def draw(self, surface, mousePos, buttonPress):
        minimizedWindows = []
        for i,v in enumerate(self.windows):
            v.draw(surface, mousePos, buttonPress, i==len(self.windows)-1)
            if v.minimized:
                minimizedWindows.append(v)
        draw.rect(surface, (240, 240, 240), (0, self.size[1] - 40, self.size[0], 40))
        for i, v in enumerate(minimizedWindows):
            windowBarRect = Rect(i * 201, self.size[1] - 40, 200, 40)
            if windowBarRect.collidepoint(mousePos):
                draw.rect(surface, (190, 190, 190), windowBarRect)
            else:
                draw.rect(surface, (200, 200, 200), windowBarRect)
            minimizedLabel = minimizedWindowFont.render(v.windowTitle,True,(255,255,255))
            surface.blit(minimizedLabel,(i*201+2, self.size[1]-20-minimizedLabel.get_height()//2))
    def addWindow(self, window):
        self.windows.append(window)

    def resize(self, newSize):
        self.size = newSize
        for i in self.windows:
            if i.maximized:
                i.unMaximize()
                i.maximize(Rect(0, 0, self.size[0], self.size[1] - 40))
