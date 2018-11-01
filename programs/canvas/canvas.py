from pygame import Surface, draw, Rect
import lib.windowedprogram
from lib import dropdown, dropdownoption


class Canvas(lib.windowedprogram.WindowedProgram):
    def configure(self):
        self.window.windowTitle = 'Canvas'
        self.window.scaleToDrawArea((800,626))
        self.window.resizable = False
        # support for multiple layers for drawing
        self.layerData.addLayer(Rect(0,0,self.availableSpace[0], self.availableSpace[1]))
    def draw(self, mousePos, mouseButtons):
        drawSurf = Surface(self.availableSpace)
        self.layerData.draw(drawSurf.subsurface(Rect(0,26,self.availableSpace[0], self.availableSpace[1]-26)))
        draw.rect(drawSurf, (240, 240, 240), (0, 0, self.availableSpace[0], 26))
        for i in self.dropdowns:
            i.draw(drawSurf, mousePos, mouseButtons)
        return drawSurf

    def update(self, mousePos, mouseButtons):
        for i in self.dropdowns:
            i.update(mousePos, mouseButtons)

    def __init__(self, availableSpace, window, additionalParams):
        super().__init__(availableSpace, window)
        self.dropdowns = []
        self.toolboxData, self.layerData = additionalParams['toolboxData'], additionalParams['layerData']
        fileDropDown = dropdown.Dropdown((0, 0), label="File")
        fileDropDown.addButton(dropdownoption.DropDownOption("New"))
        fileDropDown.addButton(dropdownoption.DropDownOption("Save"))
        fileDropDown.addButton(dropdownoption.DropDownOption("Load"))
        self.dropdowns.append(fileDropDown)
        editDropDown = dropdown.Dropdown((fileDropDown.getWidth() + 1, 0), label="Edit")
        editDropDown.addButton(dropdownoption.DropDownOption("Undo"))
        editDropDown.addButton(dropdownoption.DropDownOption("Redo"))
        self.dropdowns.append(editDropDown)
