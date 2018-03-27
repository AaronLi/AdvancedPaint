import lib.windowedprogram

class Layers(lib.windowedprogram.WindowedProgram):
    def configure(self):
        self.window.windowTitle = 'Layers'
        self.window.scaleToDrawArea((250, 600))

    def __init__(self, availableSpace, window, additionalParams):
        super().__init__(availableSpace, window)
        self.layers = additionalParams['layerData']
    def update(self, mousePos, mouseButtons):
        super().update(mousePos, mouseButtons)

    def draw(self, mousePos, mouseButtons):
        return super().draw(mousePos, mouseButtons)