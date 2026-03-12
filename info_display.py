import pygame
import json
from settings import Settings
from font import PlainText
from button import TextButton

class InfoDisplay:
    def __init__(self):
        self.settings = Settings()
        img = pygame.image.load('assets/ui_sprites/Sprites/Content Appear Animation/Paper UI Pack/Plain/5 Mini Map/1.png').convert_alpha()
        self.image = pygame.Surface((img.get_width(), img.get_height()), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect(centery = self.settings.screen_height / 2, right = self.settings.screen_width)
        self.image.blit(img, (0,0))
        # self.container = pygame.Rect((self.rect.x + 50, self.rect.y + 51), (124, 122))
        self.container = pygame.Rect((50, 60), (124, 122))
        self.active = True

    def blitme(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)
            # pygame.draw.rect(screen, (0,0,0), self.container)

class MiraclesInfoDisplay(InfoDisplay):
    def __init__(self, miracles):
        super().__init__()
        self.get_miracles(miracles)
        self.states = ['level', 'select', 'data']
        self.state = 0
        self.con = self.container.move(self.rect.topleft)
        self.miracles_title = PlainText("Miracles")
        self.miracles_title.rect.centerx = self.rect.centerx
        self.miracles_title.rect.y = self.rect.y + 40
        self.level_buttons = self.get_lv_buttons(self.container.move(self.rect.topleft))

    def get_lv_buttons(self, container):
        labels = ['Cantrips', 'Lv 1', 'Lv 2', 'Lv 3', 'Lv 4', 'Lv 5']
        arr = []
        for i, l in enumerate(labels):
            arr.append(TextButton(l, container.move(0, 18 * i)))
        return arr

    def get_miracles(self, miracles):
        self.miracles = {}
        with open("data/miracles/cantrips.json", "r") as c:
            cantrips = json.load(c)
            for m in miracles['cantrips']:
                self.miracles[cantrips[m]['name']] = cantrips[m]
        with open("data/miracles/lv1.json", "r") as m1:
            miracles1 = json.load(m1)
            for m1 in miracles['lv1']:
                self.miracles[miracles1[m1]['name']] = miracles1[m1]
    
    def update(self):
        if self.active == False:
            return
        for btn in self.level_buttons:
            btn.update()

    def check_click(self, pos=None):
        if self.active == False:
            return
        pos = pos if pos else pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if self.state == 0:
                for lv_btn in self.level_buttons:
                    val = lv_btn.check_click(pos)
                    if val:
                        print(val)
                        break
        else:
            self.active = False

    def blitme(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)
            screen.blit(self.miracles_title.text, self.miracles_title.rect)
            for btn in self.level_buttons:
                btn.blitme(screen)
