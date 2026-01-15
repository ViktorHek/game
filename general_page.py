import pygame
from pathlib import Path
import json

from page import Page
from font import Title, SmallTitle, Text, LongText
from text_box import TextBox
from input import Input

class GeneralPage(Page):
    def __init__(self, game):
        super().__init__(game)
        margin = 8
        # Left side
        self.intro_text_container = self.left_page.copy()
        self.intro_text_container.left += margin
        self.intro_text_container.top += margin * 4
        self.intro_text_container.width -= margin * 2
        self.intro_text_container.height -= margin * 8
        self.intro_text = LongText(
            "Accustomed to life underground, you have superior vision in dark and dim conditions. You can see in dim light within 60 feet of you as if it were bright light, and in darkness as if it were dim light. You can't discern color in darkness, only shades of gray.",
            self.intro_text_container
        )
        # Right side
        self.right_title = Title("General", self.right_title_container)
        self.name = ""
        self.name_input = Input("name", "Name:", (self.right_page.left, self.right_title_container.bottom + 8))

    def check_click(self):
        self.name_input.check_click()

    def update(self):
        self.name_input.update()

    def handle_key(self, key):
        name = self.name_input.handle_key(key)
        if name:
            self.name = name

    def blitme(self, screen):
        super().blitme(screen)
        screen.blit(self.right_title.image, self.right_title.rect)
        screen.blit(self.intro_text.image, self.intro_text_container)
        screen.blit(self.name_input.image, (self.right_page.left, self.right_title_container.bottom + 8))
