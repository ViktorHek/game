import pygame

class ScrollBar:
    def __init__(self, parent):
        url = "assets/ui_sprites/Sprites/Content/5 Holders/"
        self.thumb = pygame.image.load(url + "15.png")
        self.start = pygame.image.load(url + "16.png")
        self.middle = pygame.image.load(url + "17.png")
        self.end = pygame.image.load(url + "18.png")
        self.height = parent.height
        self.image = pygame.Surface((self.thumb.get_width(), self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=parent.center)
        self.render_image()

    def render_image(self):
        print(self.rect)
        x = 0
        y = 0
        self.image.blit(self.start, (x,y))
        y += self.start.get_height()
        end_height = self.end.get_height()
        while y < self.height - end_height:
            self.image.blit(self.middle, (x, y))
            y += self.middle.get_height()
        self.image.blit(self.end, (x, self.height - end_height))
        self.image.blit(self.thumb, (0, 0))
    
    