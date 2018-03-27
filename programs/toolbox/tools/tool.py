class Tool:
    def init(self):
        self.tool_enabled = False
        self.mPos = (-1, -1)
        self.oMPos = (-1, -1)
        self.surface = None
        self.mButtons = [False, False, False, False]
        self.oMButtons = [False, False, False, False]
        self.colour = (0,0,0)
        self.radius = 5
        self.fill_amount = 0
    def enable_tool(self):
        self.set_tool_enabled(True)
    def disable_tool(self):
        self.set_tool_enabled(False)
    def set_tool_enabled(self, state):
        self.tool_enabled = state
        print("Tool: %s %s"%(str(self.__class__.__name__), "enabled" if self.tool_enabled else "disabled"))
    def drawFunc(self):
        return self.tool_enabled
    def set_surface(self, surface):
        self.surface = surface
    def setMouseButtons(self, mButtons):
        self.mButtons = mButtons
    def setMousePos(self, mPos):
        self.mPos = mPos
    def set_colour(self, colour):
        self.colour = colour
    def set_radius(self, radius):
        self.radius = radius
    def set_fill(self, fill_amount):
        self.fill_amount = fill_amount
    def update(self):
        if self.tool_enabled and self.mButtons[0]:
            self.drawFunc()
        self.oMPos = self.mPos
        self.oMButtons = self.mButtons
    def mouseJustClicked(self, button = 0):
        return not self.oMButtons[button] and self.mButtons[button]
