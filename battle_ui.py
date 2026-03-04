import pygame

from settings import Settings

class BattleUI():
    def __init__(self, characters):
        self.characters = characters
        self.settings = Settings()
        self.active_index = 0
        self.cards = []
        self.current_character_id = 'player'
        self.render_characters_display()
        self.render_current_character()
        # self.action_pannel = pygame.Surface(())

    def render_characters_display(self):
        index = 0
        self.cards = []
        for key in self.characters.keys():
            self.cards.append(CharacterCard(key, index, index == self.active_index))
            index += 1
        card_width = self.cards[0].rect.width
        self.characters_display = pygame.Surface((len(self.cards) * card_width, card_width), pygame.SRCALPHA).convert_alpha()
        self.characters_display_rect = self.characters_display.get_rect(centerx = self.settings.screen_width / 2, y = 2)
        for i, card in enumerate(self.cards):
            self.characters_display.blit(card.image, (card_width * i, 0))

    def render_current_character(self):
        self.character_display = pygame.Surface((300,64), pygame.SRCALPHA).convert_alpha()
        self.character_display_rect = self.character_display.get_rect(left = 10, bottom = self.settings.screen_height - 10)
        name_font = pygame.font.Font('freesansbold.ttf', 22)
        data_font = pygame.font.Font('freesansbold.ttf', 18)
        name_text = self.characters[self.current_character_id].id.capitalize()
        name = name_font.render(name_text, True, (0,0,0))
        data_text = data_font.render('Lv 7 Betuttad Monk', True, (0,0,0))
        for c in self.cards:
            if c.id == self.current_character_id:
                img = c.portret
        self.character_display_img_rect = img.get_rect()
        self.character_display.blit(img, self.character_display_img_rect)
        self.character_display.blit(name, name.get_rect(x = self.character_display_img_rect.right + 8, top = self.character_display_img_rect.top + 14))
        self.character_display.blit(data_text, data_text.get_rect(x = self.character_display_img_rect.right + 8, top = self.character_display_img_rect.top + 36))

    def update(self):
        self.active_index += 1
        self.render_characters_display()

    def blitme(self, screen):
        screen.blit(self.characters_display, self.characters_display_rect)
        screen.blit(self.character_display, self.character_display_rect)

    def handle_action(self):
        pass

    def handle_click(self):
        pass

class CharacterCard:
    def __init__(self, id, index, is_active=False):
        images = [
            "assets/ui_sprites/character/Frame 19.png",
            "assets/ui_sprites/character/Frame 20.png",
            "assets/ui_sprites/character/Frame 21.png",
            "assets/ui_sprites/character/Frame 22.png",
            "assets/ui_sprites/character/Frame 23.png",
            "assets/ui_sprites/character/Frame 24.png",
        ]
        self.id = id
        self.index = index
        self.is_active = is_active
        bg_img = pygame.image.load('assets/ui_sprites/Sprites/Content/5 Holders/20250420manaSoul9SlicesB-Sheet.png').convert_alpha()
        self.bg = pygame.transform.scale(bg_img, (76,76))
        active_bg_img = pygame.image.load('assets/ui_sprites/Sprites/Content/5 Holders/20250420manaSoul9SlicesC-Sheet.png').convert_alpha()
        self.active_bg = pygame.transform.scale(active_bg_img, (76,76))
        self.image = pygame.Surface((76,76), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        if is_active:
            self.image.blit(self.active_bg, (0,0))
        else:
            self.image.blit(self.bg, (0,0))
        portret = pygame.image.load(images[index]).convert_alpha()
        self.portret = pygame.transform.scale(portret, (64,64))
        self.portret_rect = self.portret.get_rect(center = self.rect.center)
        self.image.blit(self.portret, self.portret_rect)

    def change_state(self):
        if self.is_active:
            self.image.blit(self.bg, (0,0))
            self.image.blit(self.portret, self.portret_rect)
            self.is_active = False
        else:
            self.image.blit(self.active_bg, (0,0))
            self.image.blit(self.portret, self.portret_rect)
            self.is_active = True
