import pygame
from pathlib import Path
import json

from page import Page
from font import Title
from button import CheckBoxList
from text_box import TextBox
from scroll_bar import ScrollBar

class ReligionPage(Page):
    def __init__(self, game):
        super().__init__(game)
        classes_path = Path("data/classes.json")
        self.db_classes = json.loads(classes_path.read_text())
        self.right_title = Title("Faith", self.right_title_container)
        self.left_title = Title("Info", self.left_title_container)

        self.text_box_container = self.right_page.copy()
        info_text = "Faith effect everything from spells, abilities and personality. You can change your religion later."
        self.text_box = TextBox(self.game, info_text, self.text_box_container)
        self.text_box.rect.bottom = self.right_page.bottom

        self.check_box_container = self.right_page.copy()
        margin = self.right_title.rect.height + 16
        self.check_box_container.y += margin
        self.check_box_container.height = self.right_page.height - self.right_title_container.height - self.text_box.rect.height
        self.class_list = self.get_class_list()
        self.check_box_list = CheckBoxList(
            self.game, 
            self.check_box_container,
            self.class_list
        )
        self.scroll_bar_container = pygame.Rect(
            (self.right_page.right - 16, self.right_title_container.bottom), 
            (16, self.check_box_container.height)
        )
        self.scroll_bar = ScrollBar(self.scroll_bar_container)

    def get_class_list(self):
        arr = []
        for key, value in self.db_classes.items():
            arr.append({"id": key, "text": value["name"], "data": value})
        return arr

    def update(self):
        self.check_box_list.update()

    def blitme(self, screen):
        super().blitme(screen)
        screen.blit(self.right_title.image, self.right_title.rect)
        screen.blit(self.left_title.image, self.left_title.rect)
        self.check_box_list.draw_list(screen)
        screen.blit(self.scroll_bar.image, self.scroll_bar.rect)
        screen.blit(self.text_box.image, self.text_box.rect)

