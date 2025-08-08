import pygame as pg
import settings

class Hazard(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        """
        A hazard area. Inherits directly from pg.sprite.Sprite.
        """
        super().__init__()
        self.image = pg.Surface((w, h))
        self.image.fill(settings.C_HAZARD)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
