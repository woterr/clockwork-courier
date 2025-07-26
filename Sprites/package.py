import pygame as pg
import settings

class Package(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        try:
            original_image = pg.image.load(settings.BACKPACK).convert_alpha()
            width = original_image.get_width()
            height = original_image.get_height()
            self.image = pg.transform.scale(original_image, (width*settings.SCALE_FACTOR, height*settings.SCALE_FACTOR))

        except pg.error:
            self.image = pg.Surface((20 * settings.SCALE_FACTOR, 20 * settings.SCALE_FACTOR))
            self.image.fill(settings.C_PACKAGE)

        self.rect = self.image.get_rect()
        self.rect.center = pos