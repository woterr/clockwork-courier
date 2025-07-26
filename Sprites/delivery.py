import pygame as pg
import settings

class DeliveryPoint(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((30, 30))
        self.image.fill(settings.C_DELIVERY)
        self.rect = self.image.get_rect()
        self.rect.center = pos