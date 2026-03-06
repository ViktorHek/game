import pygame

from character import Character

class Ally(Character):
    def __init__(self, id, pos):
        super().__init__()
        self.id = id
        self.rect.x = self.size * pos[0]
        self.rect.y = self.size * pos[1]
        self.frames = {
            'idle': self.load_animation('idle'),
            'attack': self.load_animation('attack')
        }

    def load_animation(self, type):
        arr = []
        types = {
            'idle': 'assets/tileset/Characters/Human/IDLE/base_idle_strip9.png',
            'attack': 'assets/tileset/Characters/Human/ATTACK/base_attack_strip10.png'
        }
        distance_between_frames = 192
        frame_amount = self.get_img(types[type]).get_width() / distance_between_frames
        for i in range(0, int(frame_amount)):
            s = pygame.Surface((160, 96), pygame.SRCALPHA).convert_alpha()
            x = (i * distance_between_frames + 16) * -1
            y = -16
            img = self.get_img(types[type])
            s.blit(img, (x, y))
            arr.append(s)
        return arr
