import pygame as pg
import settings

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()

        try:
            self.image = pg.image.load(image_path).convert_alpha()
        except pg.error:
            print(f"Warning: Could not load image at '{image_path}'. Using a fallback surface.")
            self.image = pg.Surface((50, 50))
            self.image.fill(settings.C_PLATFORM)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.mask = pg.mask.from_surface(self.image)

class MovingPlatform(Platform):
    def __init__(self, x, y, image_path, move_range):
        super().__init__(x, y, image_path)

        self.move_range = move_range
        self.start_x = x
        self.vel = pg.math.Vector2(2, 0)

    def update(self):
        self.rect.x += self.vel.x
        if self.rect.x > self.start_x + self.move_range or self.rect.x < self.start_x:
            self.vel.x *= -1