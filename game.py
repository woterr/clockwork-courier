import pygame as pg
import settings
import random
import settings
from Sprites.player import Player
from Sprites.platform import Platform, MovingPlatform
from Sprites.hazard import Hazard
from Sprites.steam_vent import SteamVent
from Sprites.package import Package
from Sprites.delivery import DeliveryPoint

class Game():

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pg.display.set_caption(settings.TITLE)
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
            Platform(0, settings.SCREEN_HEIGHT - 40, settings.SCREEN_WIDTH, 40),
            Platform(450, settings.SCREEN_HEIGHT - 350, 200, 20),
            Platform(50, 250, 100, 20),
            MovingPlatform(200, settings.SCREEN_HEIGHT - 150, 150, 20, 200),
            Hazard(500, settings.SCREEN_HEIGHT - 60, 100, 20),
            SteamVent(100, settings.SCREEN_HEIGHT - 60, 40, 20)
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
            (100, 220), (550, settings.SCREEN_HEIGHT - 380), (300, settings.SCREEN_HEIGHT - 180)
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
            self.clock.tick(settings.FPS)
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
        if pg.sprite.spritecollide(self.player, self.steam_vents, False): self.player.vel.y = settings.STEAM_VENT_STRENGTH

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
                if event.key in [pg.K_x, pg.K_LSHIFT]: self.player.dash()

    def draw(self):
        self.screen.fill(settings.C_BACKGROUND)
        self.all_sprites.draw(self.screen)

        if self.player.dashing:
            dash_ghost = self.player.image.copy()
            dash_ghost.fill(settings.C_DASH, special_flags=pg.BLEND_RGBA_MULT)
            self.screen.blit(dash_ghost, self.player.rect)

        score_text = self.font.render(f"Score: {self.score}", True, settings.C_TEXT)
        self.screen.blit(score_text, (10, 10))

        pg.display.flip()