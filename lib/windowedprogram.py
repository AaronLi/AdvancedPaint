from pygame import Surface
class WindowedProgram:
    def __init__(self,availableSpace, window, name='Unnamed'):
        self.name = name
        self.window = window
        self.window.windowTitle = self.name
        self.availableSpace = availableSpace
    def draw(self, mousePos, mouseButtons):
        outSurf = Surface(self.availableSpace)
        outSurf.fill((255,0,255))
        return outSurf
    def update(self, mousePos, mouseButtons):
        pass
    def resize(self, newSize):
        self.availableSpace = newSize
    def configure(self):
        pass