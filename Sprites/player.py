import pygame as pg
import settings
from spritesheet import Spritesheet

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()

        self.pos = settings.vec(50, settings.SCREEN_HEIGHT - 50)
        self.vel = settings.vec(0,0)
        self.acc = settings.vec(0,0)

        self.has_package = False

        self.direction = 1
        self.dashing = False
        self.dash_time = 0
        self.can_dash = True
        self.last_dash_time = 0

    def load_images(self):
        """ Load all the animation frames from the sprite sheet. """
        spritesheet_normal = Spritesheet(settings.CHARACTER)
        spritesheet_backpack = Spritesheet(settings.CHARACTER_BACKPACK)
        SPRITE_WIDTH = 22
        SPRITE_HEIGHT = 30

        self.idle_frames = [spritesheet_normal.get_image(0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)]
        self.walk_frames_r = [
            spritesheet_normal.get_image(SPRITE_WIDTH * 1, 0, SPRITE_WIDTH, SPRITE_HEIGHT),
            spritesheet_normal.get_image(SPRITE_WIDTH * 2, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
        ]
        self.walk_frames_l = [pg.transform.flip(frame, True, False) for frame in self.walk_frames_r]

        self.idle_frames_carrying = [spritesheet_backpack.get_image(0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)]
        self.idle_frames_carrying = [spritesheet_backpack.get_image(0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)]
        self.walk_frames_r_carrying = [
            spritesheet_backpack.get_image(SPRITE_WIDTH * 1, 0, SPRITE_WIDTH, SPRITE_HEIGHT),
            spritesheet_backpack.get_image(SPRITE_WIDTH * 2, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
        ]
        self.walk_frames_l_carrying = [pg.transform.flip(frame, True, False) for frame in self.walk_frames_r_carrying]

    def animate(self):
        now = pg.time.get_ticks()
        is_moving = abs(self.vel.x) > 0.1

        if is_moving:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)

                if self.vel.x > 0:
                    if self.has_package: self.image = self.walk_frames_r_carrying[self.current_frame]
                    else: self.image = self.walk_frames_r[self.current_frame]
                else:
                    if self.has_package: self.image = self.walk_frames_l_carrying[self.current_frame]
                    else: self.image = self.walk_frames_l[self.current_frame]

        if not is_moving:
            if self.has_package: self.image = self.idle_frames_carrying[0]
            else: self.image = self.idle_frames[0]

        bottom = self.rect.bottom
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        

    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1

        if hits:
            self.vel.y = settings.P_JMP

    def dash(self):
        now = pg.time.get_ticks()
        if self.can_dash and now - self.last_dash_time > settings.DASH_COOLDOWN:
            self.dashing = True
            self.dash_time = now
            self.last_dash_time = now
            self.vel = settings.vec(self.direction*settings.DASH_SPEED, 0)
            self.can_dash = False

    def update(self):
        self.animate()
        now = pg.time.get_ticks()

        if self.dashing:
            if now - self.dash_time > settings.DASH_DURATION:
                self.dashing = False
                self.vel.x = 0

            self.pos += self.vel
            self.rect.midbottom = self.pos
            return


        self.acc = settings.vec(0, settings.P_GRV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -settings.P_ACC
            self.direction = -1
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = settings.P_ACC
            self.direction = 1

        self.acc.x += self.vel.x*settings.P_FRI 
        self.vel += self.acc
        self.pos += self.vel + 0.5*(self.acc)

        # Prevent screen overflow
        if self.pos.x > settings.SCREEN_WIDTH - self.rect.width/2:
            self.pos.x = settings.SCREEN_WIDTH - self.rect.width / 2
        if self.pos.x < 0 + self.rect.width / 2:
            self.pos.x = 0 + self.rect.width / 2

        self.rect.midbottom = self.pos
