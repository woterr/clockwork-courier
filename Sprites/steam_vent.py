import pygame as pg
import settings

class SteamVent(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pg.Surface((w, h))
        # Making the vent a visible color for debugging purposes
        self.image.fill(settings.C_STEAM_VENT) 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
