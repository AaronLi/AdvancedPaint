from pygame import Surface
class WindowedProgram:
    def __init__(self,availableSpace, window, additionalParams = {}):
        self.name = additionalParams['name'] if 'name' in additionalParams else 'unnamed'
        self.window = window
        self.window.windowTitle = self.name
        self.availableSpace = availableSpace
        self.kwargs = additionalParams
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