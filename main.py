import pygame as pg
import sys
from game import Game

if __name__ == "__main__":
    g = Game()
    while g.running:
        g.new()

    pg.quit()
    sys.exit()