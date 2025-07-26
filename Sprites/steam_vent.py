import settings
from Sprites.platform import Platform

class SteamVent(Platform):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.image.fill(settings.C_STEAM_VENT)