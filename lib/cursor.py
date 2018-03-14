from pygame import transform

class Cursor:
    def __init__(self, sprite, center_lr=False, center_ud=False):
        self.center_lr = center_lr
        self.center_ud = center_ud
        self.sprite = sprite

    def draw(self, surface, mousePos, scale = 1):
        blitX = mousePos[0]
        blitY = mousePos[1]
        if self.center_lr:
            blitX -= self.sprite.get_width()*scale // 2
        elif self.center_ud:
            blitY -= self.sprite.get_height()*scale // 2
        surface.blit(transform.smoothscale(self.sprite,(int(self.sprite.get_width()*scale), int(self.sprite.get_height()*scale))), (blitX, blitY))
