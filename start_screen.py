import pygame

from button import Button, CheckBox, CheckBoxList
from animation import Animation, AnimationIndex
from font import Text, Title
from book import Book

class StartScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.width = self.screen_rect.width
        self.height = self.screen_rect.height
        self.image = pygame.image.load('assets/ui_sprites/Sprites/Book Desk/3.png')
        self.rect = self.image.get_rect()
        # self.left_box = pygame.Surface(80.0, self.screen_rect.width / 2, self.rect.width - 50, self.rect.height - 20)
        self.right_box = pygame.Surface((292, 365))
        self.left_box = pygame.Surface((292, 365))
        self.papper = ''
        self.rect.center = self.screen_rect.center
        self.generate_buttons()
        self.animation = Animation(
            game, AnimationIndex.header.value, (None, 50)
        )
        self.game.animations.add(self.animation)
        self.title = Title('Akavir: God of None', self.animation.rect.center, has_underline=True)
        self.text = Text('test', (350, 200), has_underline=True)
        self.text_2 = Text('testing longer word, jwoefhweofhwoi', (350, 250), has_underline=True)
        self.book = Book(self)
        self.right_page = pygame.Rect((534, 90),(270, 358))
        self.check_box_list = CheckBoxList(
            self.game, self.right_page,
            [
                {"id":"munk", "text":"Munk"},
                {"id":"cleric", "text":"Cleric"},
                {"id":"priest", "text":"Priest"},
            ] 
        )
        # self.check_box = CheckBox(self.game, "munk", "Munk", self.right_page)
        

    def generate_buttons(self):
        buttons = ['New Game', 'Load Game', 'Options']
        dummy = Button(self.game, 1337, "dummy", pygame.Rect(10,10,10,10))
        box = dummy.image.get_rect(center=self.screen_rect.center)
        box.y -= 70
        for i, button in enumerate(buttons):
            self.game.buttons.add(Button(self.game, i + 1, button, box))
            box.y += 70

    def blitme(self):
        fade = pygame.Surface((self.width, self.height))
        fade.fill((0, 0, 0))
        fade.set_alpha(160)
        self.screen.blit(fade, (0, 0))
        self.screen.blit(self.image, self.rect)
        if self.game.character_creation:
            self.book.blitme(self.screen)
            self.text.blitme(self.screen)
            self.text_2.blitme(self.screen)
        else:
            self.game.buttons.draw(self.game.screen)
            for btn in self.game.buttons:
                btn.draw_button()
            self.animation.blitme(self.game.screen)
            if self.animation.animation_is_done:
                self.title.blitme(self.screen)
        # self.check_box.draw_button()
        self.check_box_list.draw_list()