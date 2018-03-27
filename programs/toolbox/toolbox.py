import lib.windowedprogram
from pygame import image

pen_icon = image.load('img/tools/pencil.png').convert_alpha()
line_icon = image.load('img/tools/line.png').convert_alpha()


class Toolbox(lib.windowedprogram.WindowedProgram):
    def configure(self):
        self.window.windowTitle = 'Toolbox'
        self.window.scaleToDrawArea((250, 600))

    def __init__(self, availableSpace, window, additionalParams):
        super().__init__(availableSpace, window)
        self.toolboxData = additionalParams['toolboxData']

    def update(self, mousePos, mouseButtons):
        super().update(mousePos, mouseButtons)

    def draw(self, mousePos, mouseButtons):
        return super().draw(mousePos, mouseButtons)
