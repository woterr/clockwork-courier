import pygame as pg
# Constants 
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
TITLE = "The Clockwork Courier"
SCALE_FACTOR = 3
CHARACTER = "./media/character_walk_idle.png"
CHARACTER_BACKPACK = "./media/character_walk_idle_backpack.png"
BACKPACK = "./media/backpack.png"

# Colors - Some colors are temporary
C_BACKGROUND = (78, 59, 49)
C_CHARACTER = (217, 182, 141)
C_PLATFORM = (139, 91, 41)
C_HAZARD = (255, 107, 107)
C_STEAM_VENT = (217, 247, 255)
C_PACKAGE = (255, 224, 102)
C_DELIVERY = (126, 204, 126)
C_TEXT = (255, 255, 255)
C_DASH = (255, 255, 255, 128)

# Physics
P_ACC = 0.5 #               ACCELERATION
P_FRI = -0.10 #             FRICTION
P_GRV = 0.8 #               GRAVITY
P_JMP = -20 #               JUMP STRENGTH
STEAM_VENT_STRENGTH = -30#  STEAM STRENGTH
DASH_SPEED = 15#            DASHING SPEED
DASH_DURATION = 150#        DASHING DURATION
DASH_COOLDOWN = 500#        DASHING COOLDOWN

vec = pg.math.Vector2