import pygame

class Player():
    def __init__(self, game):
        self.player_size = 16
        self.game = game
        self.size = game.settings.tile_size
        self.image = pygame.image.load('assets/New Piskel-1.bmp')
        self.rect = self.image.get_rect()
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.rect.x = game.settings.tile_size * 10
        self.rect.y = game.settings.tile_size * 10
        self.speed = 1
        self.inventory = []
    
    def blitme(self):
        self.game.screen.blit(self.image, self.rect)
    
    def update(self):
        if self.moving_right:
            self.rect.x += self.speed
        if self.moving_left:
            self.rect.x -= self.speed
        if self.moving_down:
            self.rect.y += self.speed
        if self.moving_up:
            self.rect.y -= self.speed
