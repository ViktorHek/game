import pygame

class Image(pygame.sprite.Sprite):
    def __init__(self, src, parent=None, scale=1):
        super().__init__()
        img = pygame.image.load(src).convert_alpha()
        self.image = pygame.transform.scale(img, (
            img.get_width() * scale, img.get_height() * scale
        ))
        self.rect = self.image.get_rect()
        self.surf = pygame.Surface((self.image.get_width(), self.image.get_height()), pygame.SRCALPHA).convert_alpha()
        self.surf.blit(self.image, (0,0))
        if parent:
            self.rect = self.image.get_rect(center = parent.center)

    def move(self, pos):
        self.rect.center = pos