from pygame import Surface, draw
import lib.windowedprogram
from programs.canvas.lib import dropdown, dropdownoption
class Canvas(lib.windowedprogram.WindowedProgram):
    def configure(self):
        self.window.scaleToDrawArea((800,626))
        self.window.resizable = False
        self.canvases = [Surface((self.availableSpace[0], self.availableSpace[1]-26))]
        self.canvases[0].fill((255, 255, 255))
    def draw(self, mousePos, mouseButtons):
        drawSurf = Surface(self.availableSpace)
        for i in self.canvases:
            drawSurf.blit(i,(0,26))
        draw.rect(drawSurf, (240, 240, 240), (0, 0, self.availableSpace[0], 26))
        for i in self.dropdowns:
            i.draw(drawSurf, mousePos, mouseButtons)
        return drawSurf

    def update(self, mousePos, mouseButtons):
        for i in self.dropdowns:
            i.update(mousePos, mouseButtons)

    def __init__(self, availableSpace, window, name='Canvas'):
        super().__init__(availableSpace, window, name)

        self.canvas = None
        self.dropdowns = []
        self.currentCanvas = 0
        fileDropDown = dropdown.Dropdown((0,0),label="File")
        fileDropDown.addButton(dropdownoption.DropDownOption("New"))
        fileDropDown.addButton(dropdownoption.DropDownOption("Save"))
        fileDropDown.addButton(dropdownoption.DropDownOption("Load"))
        self.dropdowns.append(fileDropDown)
        editDropDown = dropdown.Dropdown((fileDropDown.getWidth()+1, 0), label="Edit")
        editDropDown.addButton(dropdownoption.DropDownOption("Undo"))
        editDropDown.addButton(dropdownoption.DropDownOption("Redo"))
        self.dropdowns.append(editDropDown)
    def getCanvases(self):
        return self.canvases
    def getCurrentCanvas(self):
        return self.canvases[self.currentCanvas]