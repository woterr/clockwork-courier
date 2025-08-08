import pygame as pg
import json
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
        self.level_data = self.load_level_data()
        self.current_level_index = 0
        self.background_image = None

    def load_level_data(self):
        try:
            with open('levels.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("ERROR: 'levels.json' not found. Make sure it's in the correct directory.")
            self.running = False
            return None
        except json.JSONDecodeError:
            print("ERROR: Could not parse levels.json. Check for syntax errors.")
            self.running = False
            return None

    def load_level(self):
        self.all_sprites.empty()
        self.platforms.empty()
        self.hazards.empty()
        self.steam_vents.empty()
        self.packages.empty()
        self.delivery_points.empty()

        self.all_sprites.add(self.player)

        if not self.level_data or self.current_level_index >= len(self.level_data['levels']):
            print("No more levels to load or level data is missing.")
            self.playing = False
            return 
        
        level = self.level_data['levels'][self.current_level_index]

        try:
            self.background_image = pg.image.load(level['background']).convert()
            self.background_image = pg.transform.scale(self.background_image, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        except (pg.error, FileNotFoundError) as e:
            print(f"Warning: Could not load background '{level['background']}'. Error: {e}. Using solid color.")
            self.background_image = None

        for p in level.get('platforms', []):
            plat = Platform(p['x'], p['y'], p['image'])
            self.all_sprites.add(plat)
            self.platforms.add(plat)

        # Load moving platforms using image paths
        for p in level.get('moving_platforms', []):
            plat = MovingPlatform(p['x'], p['y'], p['image'], p['range'])
            self.all_sprites.add(plat)
            self.platforms.add(plat)

        for h in level.get('hazards', []):
            hazard = Hazard(h['x'], h['y'], h['w'], h['h'])
            self.all_sprites.add(hazard)
            self.hazards.add(hazard)

        for v in level.get('steam_vents', []):
            vent = SteamVent(v['x'], v['y'], v['w'], v['h'])
            self.all_sprites.add(vent)
            self.steam_vents.add(vent)


        floor = pg.sprite.Sprite()
        floor.rect = pg.Rect(0, settings.SCREEN_HEIGHT - 1, settings.SCREEN_WIDTH, 10)
        self.platforms.add(floor)

        self.spawn_points = level.get('spawn_points', [])
        self.spawn_delivery()

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

        self.load_level()
        self.run()

    def advance_level(self):
        self.current_level_index += 1
        if self.current_level_index < len(self.level_data['levels']):
            print(f"Advancing level {self.current_level_index + 1}")
            self.player.pos = settings.vec(50, settings.SCREEN_HEIGHT - 50)
            self.load_level()
        else:
            print("You beat all levels! Congratulations!")
            self.playing = False

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
                self.advance_level()


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
        if self.background_image:
            self.screen.blit(self.background_image, (0,0))
        else:
            self.screen.fill(settings.C_BACKGROUND)
            
        self.all_sprites.draw(self.screen)

        if self.player.dashing:
            dash_ghost = self.player.image.copy()
            dash_ghost.fill(settings.C_DASH, special_flags=pg.BLEND_RGBA_MULT)
            self.screen.blit(dash_ghost, self.player.rect)

        score_text = self.font.render(f"Score: {self.score}", True, settings.C_TEXT)
        level_name = self.level_data['levels'][self.current_level_index]['name']
        level_text = self.font.render(level_name, True, settings.C_TEXT)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (settings.SCREEN_WIDTH - level_text.get_width() - 10, 10))
       
        pg.display.flip()