class DeskEnv:
    def __init__(self):
        self.windows = []
    def update(self):
        for i in self.windows:
            i.update()
    def draw(self):
        for i in self.windows:
            i.draw()