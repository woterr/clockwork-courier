import pygame as pg
import settings

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height), pg.SRCALPHA)
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        image = pg.transform.scale(image, (width*settings.SCALE_FACTOR, height*settings.SCALE_FACTOR))
        return image