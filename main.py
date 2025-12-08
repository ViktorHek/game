import sys
import pygame
from pytmx.util_pygame import load_pygame

from player import Player
from settings import Settings
from start_screen import StartScreen

class Main():
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Akavir: God of none')
        # self.tmxdata = load_pygame('map/example_maptmx.tmx')
        self.counter = 0
        self.game_is_running = True
        self.game_pause = True
        self.buttons = pygame.sprite.Group()
        self.animations = pygame.sprite.Group()
        self.player = Player(self)
        self.start_screen = StartScreen(self)
        self.character_creation = False

    def run(self):
        while self.game_is_running:
            self.check_event()
            if self.game_pause:
                self.buttons.update()
            else:
                self.player.update()
            self.animations.update()
            self.clock.tick(60)
            self.update_screen()

    def update_screen(self):
        self.screen.fill((100,100,100))
        # self.blit_all_tiles()
        self.screen.blit(self.player.image, self.player.rect)
        if self.game_pause:
            self.start_screen.blitme()
        pygame.display.flip()

    # def blit_all_tiles(self):
    #     for i, layer in enumerate(self.tmxdata):
    #         for tile in layer.tiles():
    #             x_pixel = tile[0] * self.settings.tile_size
    #             y_pixel = tile[1] * self.settings.tile_size
    #             img = pygame.transform.scale(tile[2], (self.settings.tile_size, self.settings.tile_size))
    #             self.screen.blit(img, (x_pixel, y_pixel))

    def check_event(self):
        for event in pygame.event.get():
            self.check_movement()
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click()

    def check_movement(self):
        keys = pygame.key.get_pressed()
        self.player.moving_down = keys[pygame.K_DOWN]
        self.player.moving_up = keys[pygame.K_UP]
        self.player.moving_right = keys[pygame.K_RIGHT]
        self.player.moving_left = keys[pygame.K_LEFT]

    def handle_click(self):
        for btn in self.buttons:
            id = btn.check_click()
            if id == 1:
                self.character_creation = True
            elif id == 2:
                self.game_pause = False
            

if __name__ == '__main__':
    game = Main()
    game.run()
    pygame.quit()
