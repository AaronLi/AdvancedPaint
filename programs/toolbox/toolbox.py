import lib.windowedprogram
class Toolbox(lib.windowedprogram.WindowedProgram):
    def configure(self):
        self.window.scaleToDrawArea((250,600))
    def __init__(self, availableSpace, window, name='Toolbox'):
        super().__init__(availableSpace, window, name)

    def update(self, mousePos, mouseButtons):
        super().update(mousePos, mouseButtons)

    def draw(self, mousePos, mouseButtons):
        return super().draw(mousePos, mouseButtons)