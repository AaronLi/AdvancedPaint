from pygame import Surface, SRCALPHA, Rect

# A layer is a list with 2 elements in it, [position(x, y), Surface]
class LayerData:
    def __init__(self):
        self.layers = []
        self.currentLayer = None

    def insertLayer(self, index, dimensions: Rect, fill_colour=(255, 255, 255)):
        temp = Surface(dimensions.size, SRCALPHA)
        temp.fill(fill_colour)
        self.layers.insert(index, [dimensions.topleft, temp])
        self.currentLayer = temp
        print("New layer of size", dimensions.size, "added with colour",fill_colour)
        return self
    def addLayer(self, dimensions: Rect, fill_colour=(255, 255, 255)):
        self.insertLayer(len(self.layers), dimensions, fill_colour)
        return self
    def draw(self, surface):
        layerRects = []
        farthestTopLeftCorner = [0, 0]
        for i in self.layers:
            layerRect = Rect(i[0][0], i[0][1], i[1].get_width(), i[1].get_height())
            layerRects.append(layerRect)
            farthestTopLeftCorner[0] = min(farthestTopLeftCorner[0], i[0][0])
            farthestTopLeftCorner[1] = min(farthestTopLeftCorner[1], i[0][1])
        masterRect = Rect(0,0,0,0).unionall(layerRects)
        mainSurface = Surface(masterRect.size, SRCALPHA)
        for i in self.layers:
            mainSurface.blit(i[1], (i[0][0]-farthestTopLeftCorner[0], i[0][1]-farthestTopLeftCorner[1]))
        surface.blit(mainSurface, farthestTopLeftCorner)