import pygame as pg
import sys

# Constants 

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "The Clockwork Courier"

# Colors
C_BACKGROUND = (78, 59, 49)
C_CHARACTER = (217, 182, 141)
C_PLATFORM = (139, 91, 41)

# Physics
P_ACC = 0.5 #       ACCELERATION
P_FRI = -0.12 #     FRICTION
P_GRV = 0.8 #       GRAVITY
P_JMP = -20 #       JUMP STRENGTH

vec = pg.math.Vector2

# PLAYER
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        self.image = pg.Surface((30, 40))
        self.image.fill(C_CHARACTER)
        self.rect = self.image.get_rect()

        self.pos = vec(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        self.on_ground = False

    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1

        if hits:
            self.vel.y = P_JMP

    def update(self):
        self.acc = vec(0, P_GRV)

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -P_ACC
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = P_ACC

        # Apply friction to slow down
        self.acc.x += self.vel.x*P_FRI

        # Update velocity based on acc
        self.vel += self.acc
        
        # Update position based on velocity
        self.pos += self.vel + 0.5*(self.acc)

        # Prevent screen overflow
        if self.pos.x > SCREEN_WIDTH - self.rect.width/2:
            self.pos.x = SCREEN_WIDTH - self.rect.width / 2
        if self.pos.x < 0 + self.rect.width / 2:
            self.pos.x = 0 + self.rect.width / 2

        
        self.rect.midbottom = self.pos


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()

        self.image = pg.Surface((w, h))
        self.image.fill(C_PLATFORM)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()

        # create player
        self.player = Player(self)
        self.all_sprites.add(self.player)

        level_layout = [
            (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40), # Ground floor
            (200, SCREEN_HEIGHT - 200, 150, 20),      # Mid-level platform
            (450, SCREEN_HEIGHT - 350, 200, 20),      # High platform
            (50, 250, 100, 20)                        # Floating left platform
        ]

        for plat_data in level_layout:
            p = Platform(*plat_data)
            self.all_sprites.add(p)
            self.platforms.add(p)

        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

        # Physics engine
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                highest_platform = hits[0]
                for hit in hits:
                    if hit.rect.top > highest_platform.rect.top:
                        highest_platform = hit

                if self.player.pos.y < highest_platform.rect.bottom:
                    self.player.pos.y = highest_platform.rect.top + 1
                    self.player.vel.y = 0

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_UP or event.key == pg.K_w:
                    self.player.jump()

    def draw(self):
        self.screen.fill(C_BACKGROUND)
        self.all_sprites.draw(self.screen)

        pg.display.flip()


if __name__ == "__main__":
    g = Game()
    while g.running:
        g.new()

    pg.quit()
    sys.exit()