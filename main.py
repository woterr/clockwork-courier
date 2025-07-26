import pygame as pg
import sys
import random

# Constants 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "The Clockwork Courier"

# Colors
C_BACKGROUND = (78, 59, 49)
C_CHARACTER = (217, 182, 141)
C_PLATFORM = (139, 91, 41)
C_HAZARD = (255, 107, 107)
C_STEAM_VENT = (217, 247, 255)
C_PACKAGE = (255, 224, 102)
C_DELIVERY = (126, 204, 126)
C_TEXT = (255, 255, 255)

# Physics
P_ACC = 0.5 #       ACCELERATION
P_FRI = -0.12 #     FRICTION
P_GRV = 0.8 #       GRAVITY
P_JMP = -20 #       JUMP STRENGTH
STEAM_VENT_STRENGTH = -30

vec = pg.math.Vector2

# PLAYER
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        self.image_default = pg.Surface((30, 40))
        self.image_default.fill(C_CHARACTER)

        self.image_carrying = pg.Surface((30, 40))
        self.image_default.fill(C_CHARACTER)
        pg.draw.rect(self.image_carrying, C_PACKAGE, (5, -10, 20, 20))
        
        self.image = self.image_default
        self.rect = self.image.get_rect()

        self.pos = vec(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        self.has_package = False

    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1

        if hits:
            self.vel.y = P_JMP

    def update(self):
        self.image = self.image_carrying if self.has_package else self.image_default

        self.acc = vec(0, P_GRV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -P_ACC
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = P_ACC

        self.acc.x += self.vel.x*P_FRI 
        self.vel += self.acc
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

class MovingPlatform(Platform):
    def __init__(self, x, y, w, h, move_range):
        super().__init__(x, y, w, h)
        self.image.fill(C_PLATFORM)
        self.move_range_start = x
        self.move_range_end = x + move_range
        self.speed = 2
        self.vel = vec(self.speed, 0)

    def update(self):
        self.rect.x += self.vel.x
        if self.rect.right > self.move_range_end or self.rect.left < self.move_range_start:
            self.vel.x *= -1

class Hazard(Platform):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.image.fill(C_HAZARD)

class SteamVent(Platform):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.image.fill(C_STEAM_VENT)

class Package(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((20, 20))
        self.image.fill(C_PACKAGE)
        self.rect = self.image.get_rect()
        self.rect.center = pos

class DeliveryPoint(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((30, 30))
        self.image.fill(C_DELIVERY)
        self.rect = self.image.get_rect()
        self.rect.center = pos

class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font = pg.font.Font(None, 36)

    def new(self):
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.hazards = pg.sprite.Group()
        self.steam_vents = pg.sprite.Group()
        self.packages = pg.sprite.Group()
        self.delivery_points = pg.sprite.Group()

        # create player
        self.player = Player(self)
        self.all_sprites.add(self.player)

        level_layout = [
            Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
            Platform(450, SCREEN_HEIGHT - 350, 200, 20),
            Platform(50, 250, 100, 20),
            MovingPlatform(200, SCREEN_HEIGHT - 150, 150, 20, 200),
            Hazard(500, SCREEN_HEIGHT - 60, 100, 20),
            SteamVent(100, SCREEN_HEIGHT - 60, 40, 20)
        ]

        for item in level_layout:
            self.all_sprites.add(item)
            if isinstance(item, Hazard):
                self.hazards.add(item)
            elif isinstance(item, SteamVent):
                self.steam_vents.add(item)
            else:
                self.platforms.add(item)

        self.spawn_points = [
            (100, 220), (550, SCREEN_HEIGHT - 380), (300, SCREEN_HEIGHT - 180)
        ]
        self.spawn_delivery()
        self.run()

    def spawn_delivery(self):
        for item in self.packages: item.kill()
        for item in self.delivery_points: item.kill()

        points = random.sample(self.spawn_points, 2)
        package_pos = points[0]
        delivery_pos = points[1]

        package = Package(package_pos)
        delivery_point = DeliveryPoint(delivery_pos)

        self.all_sprites.add(package, delivery_point)
        self.packages.add(package)
        self.delivery_points.add(delivery_point)

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
                highest_platform = max(hits, key=lambda p: p.rect.top)

                if self.player.pos.y < highest_platform.rect.bottom:
                    self.player.pos.y = highest_platform.rect.top + 1
                    self.player.vel.y = 0

                    if isinstance(highest_platform, MovingPlatform):
                        self.player.pos.x += highest_platform.vel.x

        if pg.sprite.spritecollide(self.player, self.hazards, False): self.playing = False
        if pg.sprite.spritecollide(self.player, self.steam_vents, False): self.player.vel.y = STEAM_VENT_STRENGTH

        if not self.player.has_package:
            package_hits = pg.sprite.spritecollide(self.player, self.packages, True)
            if package_hits:
                self.player.has_package = True

        if self.player.has_package:
            delivery_hits = pg.sprite.spritecollide(self.player, self.delivery_points, True)
            if delivery_hits:
                self.player.has_package = False
                self.score += 100
                self.spawn_delivery()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key in [pg.K_SPACE, pg.K_UP, pg.K_w]: self.player.jump()

    def draw(self):
        self.screen.fill(C_BACKGROUND)
        self.all_sprites.draw(self.screen)

        score_text = self.font.render(f"Score: {self.score}", True, C_TEXT)
        self.screen.blit(score_text, (10, 10))

        pg.display.flip()


if __name__ == "__main__":
    g = Game()
    while g.running:
        g.new()

    pg.quit()
    sys.exit()