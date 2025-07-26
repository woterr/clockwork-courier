import pygame as pg
import settings

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pg.Surface((w, h))
        self.image.fill(settings.C_PLATFORM)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class MovingPlatform(Platform):
    def __init__(self, x, y, w, h, move_range):
        super().__init__(x, y, w, h)
        self.image.fill(settings.C_PLATFORM)
        self.move_range_start = x
        self.move_range_end = x + move_range
        self.speed = 2
        self.vel = settings.vec(self.speed, 0)

    def update(self):
        self.rect.x += self.vel.x
        if self.rect.right > self.move_range_end or self.rect.left < self.move_range_start:
            self.vel.x *= -1