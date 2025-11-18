import sys
import pygame
from pytmx.util_pygame import load_pygame

from player import Player
from settings import Settings

class Main():
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.base_tile_prop = {
            'id': -1, 'collision': 0, 'type': 'fake', 'source': '', 'trans': None, 'width': '32', 'height': '32', 'frames': []
        }
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Akavir: God of none')
        self.tmxdata = load_pygame('map/example_maptmx.tmx')
        self.counter = 0
        self.game_is_running = True
        self.player = Player(self)

    def run(self):
        while self.game_is_running:
            self.check_event()
            self.update_player()
            self.clock.tick(60)
            self.update_screen()

    def update_player(self):
        if self.player.moving_right and self.is_colliding('right'):
           self.player.rect.x -= self.player.speed
           self.player.moving_right = False
        if self.player.moving_left and self.is_colliding('left'):
           self.player.rect.x += self.player.speed
           self.player.moving_left = False
        if self.player.moving_up and self.is_colliding('up'):
           self.player.rect.y += self.player.speed
           self.player.moving_up = False
        if self.player.moving_down and self.is_colliding('down'):
           self.player.rect.y -= self.player.speed
           self.player.moving_down = False
        self.player.update()

    def is_colliding(self, dir):
        size = self.settings.tile_size
        x = self.player.rect.x + (size // 2)
        y = self.player.rect.y + (size // 2)
        extra = 10
        pos_x_1 = (x - extra) // size
        pos_x_2 = (x + extra) // size
        pos_y_1 = (y - extra) // size
        pos_y_2 = (y + extra) // size
        collision = False
        if dir == 'right':
            pos_x_1 = (x + extra) // size
        if dir == 'left':
            pos_x_2 = (x - extra) // size
        if dir == 'down':
            pos_y_1 = (y + extra) // size
        if dir == 'up':
            pos_y_2 = (y - extra) // size
        for i in range(len(self.tmxdata.layers)):
            if self.try_get_prop(pos_x_1, pos_y_1, i)['collision'] == 1:
                collision = True
            if self.try_get_prop(pos_x_2, pos_y_2, i)['collision'] == 1:
                collision = True
        return collision

    def try_get_prop(self, x, y, layer=0):
        try:
            properties = self.tmxdata.get_tile_properties(x, y, layer)
        except ValueError:
            properties = self.base_tile_prop
        if properties is None:
            properties = self.base_tile_prop
        return properties

    def update_screen(self):
        self.screen.fill((100,100,100))
        self.blit_all_tiles()
        self.player.blitme()
        pygame.display.flip()

    def blit_all_tiles(self):
        for layer in self.tmxdata:
            for tile in layer.tiles():
                x_pixel = tile[0] * self.settings.tile_size
                y_pixel = tile[1] * self.settings.tile_size
                self.screen.blit(tile[2], (x_pixel, y_pixel))

    def blit_all_overlay(self):
        y_axe = self.player.rect.y // self.settings.tile_size
        x_axe = self.player.rect.x // self.settings.tile_size
        for i, layer in enumerate(self.tmxdata):
            for tile in layer.tiles():
                is_close_x = x_axe == tile[0] or x_axe + 1 == tile[0] or y_axe == tile[0] or y_axe + 1 == tile[0]
                if i > 4 and tile[1] * self.settings.tile_size > self.player.rect.y and is_close_x:
                    x_pixel = tile[0] * self.settings.tile_size
                    y_pixel = tile[1] * self.settings.tile_size
                    self.screen.blit(tile[2], (x_pixel, y_pixel))

    def blit_all_overlay(self):
        y_axe = self.player.rect.y // self.tile_size
        x_axe = self.player.rect.x // self.tile_size
        for i, layer in enumerate(self.tmxdata):
            for tile in layer.tiles():
                is_close_x = x_axe == tile[0] or x_axe + 1 == tile[0] or y_axe == tile[0] or y_axe + 1 == tile[0]
                if i > 4 and tile[1] * self.settings.tile_size > self.player.rect.y and is_close_x:
                    x_pixel = tile[0] * self.settings.tile_size + self.world_offset[0]
                    y_pixel = tile[1] * self.settings.tile_size + self.world_offset[1]
                    self.screen.blit(tile[2], (x_pixel, y_pixel))

    def check_event(self):
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            self.player.moving_down = keys[pygame.K_DOWN]
            self.player.moving_up = keys[pygame.K_UP]
            self.player.moving_right = keys[pygame.K_RIGHT]
            self.player.moving_left = keys[pygame.K_LEFT]
            if event.type == pygame.QUIT:
                sys.exit()
            

if __name__ == '__main__':
    game = Main()
    game.run()
    pygame.quit()
