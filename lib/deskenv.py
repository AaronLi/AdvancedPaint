from pygame import Rect, draw


class DeskEnv:
    def __init__(self, size):
        self.windows = []
        self.size = size
        self.lastButtonState = (False, False, False)

    def update(self, mousePos, buttonPress):
        minimizedWindows = []
        for i in self.windows:
            i.update(mousePos, buttonPress, Rect(0, 0, self.size[0], self.size[1] - 40))
            if i.minimized and not i.closed:
                minimizedWindows.append(i)
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
        for i in self.windows:
            i.draw(surface, mousePos, buttonPress)
            if i.minimized:
                minimizedWindows.append(i)
        draw.rect(surface, (240, 240, 240), (0, self.size[1] - 40, self.size[0], 40))
        for i, v in enumerate(minimizedWindows):
            windowBarRect = Rect(i * 201, self.size[1] - 40, 200, 40)
            if windowBarRect.collidepoint(mousePos):
                draw.rect(surface, (190, 190, 190), windowBarRect)
            else:
                draw.rect(surface, (200, 200, 200), windowBarRect)

    def addWindow(self, window):
        self.windows.append(window)

    def resize(self, newSize):
        self.size = newSize
        for i in self.windows:
            if i.maximized:
                i.unMaximize()
                i.maximize(Rect(0, 0, self.size[0], self.size[1] - 40))
