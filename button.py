import pygame
from pygame.sprite import Sprite
from font import Text

class Button(Sprite):
    def __init__(self, game, id, text, parent):
        super().__init__()
        pos = parent.center
        self.game = game
        self.screen = game.screen
        self.id = id
        img = pygame.image.load('assets/button.png')
        self.wh = (img.get_rect().width * 2, img.get_rect().height * 2)
        self.image = pygame.transform.scale(img, self.wh)
        self.rect = self.image.get_rect(center = pos)
        self.text = Text(text, pos)

    def draw_button(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text.text, self.text.rect)

    def update(self):
        pos = pygame.mouse.get_pos()
        basic = pygame.image.load('assets/button.png')
        active = pygame.image.load('assets/button_hover.png')
        if self.rect.collidepoint(pos):
            self.image = pygame.transform.scale(active, self.wh)
        else:
            self.image = pygame.transform.scale(basic, self.wh)

    def check_click(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and self.game.game_pause:
            return self.id
        else:
            return False

class CheckBoxList():
    def __init__(self, game, parent, list):
        self.game = game
        self.parent = parent
        # self.box = parent
        # self.box.height = 32
        self.list = self.get_list(list)

    def get_list(self, list):
        arr = []
        box = self.parent
        box.height = 32
        for i, button in enumerate(list):
            arr.append(CheckBox(self.game, button["id"], button["text"], box))
            box.y += 32
        return arr
    
    def draw_list(self):
        for button in self.list:
            button.draw_button()
        
class CheckBox(Button):
    def __init__(self, game, id, text, parent):
        super().__init__(game, id, text, parent)
        self.width = 280
        self.height = game.settings.tile_size
        self.parent = parent
        self.is_checked = False
        self.is_active = False
        url = "assets/ui_sprites/Sprites/Content/5 Holders/"
        self.arrow = pygame.transform.flip(pygame.image.load("assets/ui_sprites/Sprites/Content/4 Buttons/Sliced/5.png"), True, False)
        self.start = pygame.image.load(url + '9.png')
        self.middle = pygame.image.load(url + '10.png')
        self.end = pygame.image.load(url + '11.png')
        self.check_box_img = pygame.image.load(url + '22.png')
        self.arrow_rect = self.arrow.get_rect(
            left=parent.left, centery=parent.centery,
        )
        self.check_box_rect = self.check_box_img.get_rect( 
            left = self.arrow_rect.right, centery=parent.centery,
        )
        self.start_rect = self.start.get_rect(
            left = self.check_box_rect.right, centery=parent.centery,
        )
        self.end_rect = self.end.get_rect(
            left=parent.right, centery=parent.centery
        )

    def draw_button(self):
        self.screen.blit(self.arrow, self.arrow_rect)
        self.screen.blit(self.check_box_img, self.check_box_rect)
        self.screen.blit(self.start, self.start_rect)
        x = self.start_rect.right
        y = self.start_rect.top
        while x < self.parent.right:
            self.screen.blit(self.middle, (x,y))
            x += self.middle.get_width()
        self.screen.blit(self.end, self.end_rect)

    # update