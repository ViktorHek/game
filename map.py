import pygame
from pytmx.util_pygame import load_pygame
from settings import Settings

class Map:
    def __init__(self):
        self.settings = Settings()
        self.tmxdata = load_pygame('map/example_maptmx.tmx')

    def blit_all_tiles(self, screen):
        for layer in self.tmxdata:
            for tile in layer.tiles():
                x_pixel = tile[0] * self.settings.tile_size
                y_pixel = tile[1] * self.settings.tile_size
                img = pygame.transform.scale(tile[2], (self.settings.tile_size, self.settings.tile_size))
                screen.blit(img, (x_pixel, y_pixel))
