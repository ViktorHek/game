import pygame
from font import Text
from tool_tip import ToolTip
from settings import Settings

class Input:
    def __init__(self, id, label, pos):
        self.id = id
        self.is_active = False
        self.pos = pos
        self.value = ""
        self.width = 288
        self.height = 32
        self.font_size = 20
        self.settings = Settings()
        self.max_letter = 18
        self.font = pygame.font.Font('assets/font/ThaleahFat.ttf', self.font_size)
        self.text = self.font.render(self.value, True, self.settings.text_color).convert_alpha()
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA).convert_alpha()
        self.label = Text(label, self.image.get_rect(width = self.image.get_width() / 2))
        self.rect = self.image.get_rect()
        url = "assets/ui_sprites/Sprites/Content/"
        self.start = pygame.image.load(url + '5 Holders/9.png').convert_alpha()
        self.middle = pygame.image.load(url + '5 Holders/10.png').convert_alpha()
        self.end = pygame.image.load(url + '5 Holders/11.png').convert_alpha()
        self.fill_surf()
        self.text_start_x = 8 + self.label.image.get_width() + 8 + self.start.get_width()
        self.text_cursor_pos = 8 + self.label.image.get_width() + 8 + self.start.get_width()
        self.text_cursor_rect = pygame.Rect((self.text_start_x, 7), (1, 17))
        self.text_cursor_counter = 0

    def blitme(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        delay = 40
        if self.is_active:
            self.text_cursor_counter += 1
            if self.text_cursor_counter == delay:
                self.fill_surf()
            elif self.text_cursor_counter == delay * 2:
                self.draw_text_cursor()
                self.text_cursor_counter = 0

    def draw_text_cursor(self):
        self.fill_surf()
        pygame.draw.rect(self.image, (0,0,0), self.text_cursor_rect)

    def check_click(self):
        pos = pygame.mouse.get_pos()
        r = self.image.get_rect(x = self.pos[0], y = self.pos[1])
        if r.collidepoint(pos):
            self.is_active = True
            self.draw_text_cursor()
        else:
            self.is_active = False
            self.fill_surf()
        
    def fill_surf(self):
        self.image.blit(self.label.image, (8, self.label.rect.y))
        x = 8 + self.label.image.get_width() + 8
        self.image.blit(self.start, (x, 0))
        x += self.start.get_width()
        while x < self.rect.right - 16 - 8:
            self.image.blit(self.middle, (x, 0))
            x += self.middle.get_width()
        self.image.blit(self.end, (self.rect.right - self.end.get_width() - 8, 0))
        self.image.blit(self.text, ((8 + self.label.image.get_width() + 8 + self.start.get_width(), 7)))

    def handle_key(self, key):
        special_keys = [
            pygame.K_BACKSPACE,
            pygame.K_SPACE,
            pygame.K_RETURN,
            pygame.K_LEFT,
            pygame.K_RIGHT
        ]
        space = 10
        if key not in self.settings.permitted_keys or self.is_active == False:
            return
        if len(self.value) == self.max_letter and key != pygame.K_BACKSPACE:
            return
        if key in special_keys:
            if key == pygame.K_SPACE:
                self.value += " "
                space = self.font.render(" ", True, self.settings.text_color).convert_alpha().get_width()
            elif key == pygame.K_BACKSPACE:
                self.value = self.value[:-1]
                space = self.font.render(self.value[-1], True, self.settings.text_color).convert_alpha().get_width() * -1
            elif key == pygame.K_RETURN:
                self.fill_surf()
                self.is_active = False
                return self.value
        else:
            self.value += pygame.key.name(key)
            space = self.font.render(pygame.key.name(key), True, self.settings.text_color).convert_alpha().get_width()
        self.text = self.font.render(self.value, True, self.settings.text_color).convert_alpha()
        self.text_cursor_rect.x += space
        self.draw_text_cursor()
        return self.value
