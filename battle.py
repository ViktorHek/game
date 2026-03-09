import sys
import pygame
from random import randrange

from player import Player
from settings import Settings
from npc import Npc
from ally import Ally
from battle_map import BattleMap
from action_wheel import ActionWheel
from battle_ui import BattleUI

class Battle():
    def __init__(self):
        self.game_pause = False
        self.walking_animation = False
        self.turn_order = []
        self.current_active_character_id = 'player'
        self.settings = Settings()
        self.map = BattleMap()
        self.player = Player([5, 10])
        self.npc_1 = Npc('jon', (6, 3))
        self.npc_2 = Npc('bob', (24, 3), type='skeleton')
        self.npc_3 = Npc('mike', (20, 11))
        self.ally_1 = Ally(id='buddy', pos=(6, 11))
        # self.get_ui()
        self.ui = BattleUI({
            f"{self.player.id}": self.player, 
            f"{self.npc_1.id}": self.npc_1, 
            f"{self.npc_2.id}": self.npc_2, 
            f"{self.npc_3.id}": self.npc_3, 
            f"{self.ally_1.id}": self.ally_1 
        })
        self.npc_group = [self.npc_1, self.npc_2, self.npc_3, self.ally_1]
        self.player_moves_amount = self.player.data.speed // 10
        self.available_tiles = [] 
        self.unavailable_tiles = []
        self.load_init_data()
        self.action_wheel_target = None
        self.action_wheel = ActionWheel()
        self.init_battle() # call from parent instead

    def get_ui(self):
        dic = {}
        for id in self.turn_order:
            if id == self.player.id:
                dic[f"{id}"] = self.player
            elif id == self.npc_1.id:
                dic[f"{id}"] = self.npc_1
            elif id == self.npc_2.id:
                dic[f"{id}"] = self.npc_2
            elif id == self.npc_3.id:
                dic[f"{id}"] = self.npc_3
            elif id == self.ally_1.id:
                dic[f"{id}"] = self.ally_1
        self.ui = BattleUI(dic)

    def init_battle(self):
        self.roll_inisiative()
        self.get_ui()

    def load_init_data(self):
        for npc in self.npc_group:
            pos = npc.get_coordinates()
            self.map.mobile_collision_grid[npc.id] = pos
        self.get_tile_availability()
        self.map.update_grid(self.available_tiles, self.unavailable_tiles)

    def roll_inisiative(self):
        arr = [self.player.id, self.npc_1.id, self.npc_2.id, self.npc_3.id, self.ally_1.id]
        dic = {}
        for char in arr:
            dic[char] = randrange(1,21)
        self.turn_order = [k for k, v in sorted(dic.items(), key=lambda item: item[1])]

    def get_tile_availability(self):
        self.available_tiles = []
        self.unavailable_tiles = []
        x = self.player.rect.x // self.settings.tile_size
        y = self.player.rect.y // self.settings.tile_size
        dirs = [
            [x - 1, y],
            [x + 1, y],
            [x, y - 1],
            [x, y + 1],
        ]
        if self.player_moves_amount:
            for pos in dirs:
                collision = self.map.get_tile_collision(pos[0], pos[1])
                if collision == None:
                    self.available_tiles.append([pos[0], pos[1]])
                else:
                    self.unavailable_tiles.append([pos[0], pos[1]])

    def update(self):
        if self.walking_animation:
            self.check_walking_animation()
        self.player.update()
        if self.action_wheel_target:
            self.action_wheel.update()

    def check_walking_animation(self):
        pos = [
            self.player.rect.x / self.settings.tile_size, 
            self.player.rect.y / self.settings.tile_size
        ]
        if pos[0] == float(self.player.moving_to[0]) and pos[1] == float(self.player.moving_to[1]):
            self.player.reset_movement()
            self.player_moves_amount -= 1
            self.player.steps_amount -= 1
            self.get_ui()
            self.walking_animation = False
            self.get_tile_availability()
            self.map.update_grid(self.available_tiles, self.unavailable_tiles)

    def blitme(self, screen):
        self.map.blit_all_tiles(screen)
        for npc in self.npc_group:
            npc.blitme(screen)
        self.player.blitme(screen)
        self.map.blit_spacing_grid(screen)
        self.ui.blitme(screen)
        if self.player_moves_amount > 0:
            circle_radius = self.player_moves_amount * self.settings.tile_size + self.player.rect.width // 2
            pygame.draw.circle(screen, (0,0,255), self.player.rect.center, circle_radius, width=2)
        if self.action_wheel_target:
            self.action_wheel.blitme(screen)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEWHEEL:
            pass # scroll_down = True if event.y < 0 else False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click()
        elif event.type == pygame.KEYDOWN:
            self.handle_key(event.key, True)
        elif event.type == pygame.KEYUP:
            self.handle_key(event.key, False)

    def handle_key(self, key, is_down):
        if key == pygame.K_SPACE:
            if is_down:
                self.handle_action()
        elif key == pygame.K_p:
            self.game_pause = True
        elif key == pygame.K_q:
            self.end_turn()
        elif key == pygame.K_RIGHT or key == pygame.K_LEFT or key == pygame.K_UP or key == pygame.K_DOWN:
            self.handle_movement(key, is_down)

    def handle_movement(self, key, is_down):
        if is_down or self.player_moves_amount < 1:
            return
        x = self.player.rect.x // self.settings.tile_size
        y = self.player.rect.y // self.settings.tile_size
        is_moving = False
        if key == pygame.K_RIGHT:
            if [x + 1, y] in self.available_tiles:
                x += 1
                is_moving = True
        elif key == pygame.K_LEFT:
            if [x - 1, y] in self.available_tiles:
                x -= 1
                is_moving = True
        elif key == pygame.K_DOWN:
            if [x, y + 1] in self.available_tiles:
                y += 1
                is_moving = True
        elif key == pygame.K_UP:
            if [x, y - 1] in self.available_tiles:
                y -= 1
                is_moving = True
        if self.walking_animation == False and is_moving:
            self.walking_animation = True
            self.player.moving_to = [x, y]
            self.player.handle_movement(key, True)

    def handle_action(self):
        pass

    def melee_attack(self, id):
        self.current_active_character_id # person attacking
        for npc in self.npc_group:
            if npc.id == id:
                npc.take_damage(1, 'bludgeoning')

    def handle_action_wheel(self, action_obj):
        if action_obj['val'] == 'primary':
            self.melee_attack(action_obj['id'])
            self.player.actions_amount -= 1
            self.get_ui()
            if self.player.actions_amount < 1 and self.player.bonus_action_amount < 1 and self.player.steps_amount < 1:
                self.end_turn()

    def end_turn(self):
        for i, x in enumerate(self.turn_order):
            if x == self.current_active_character_id:
                if i == len(self.turn_order) - 1:
                    self.current_active_character_id = self.turn_order[0]
                else:
                    self.current_active_character_id = self.turn_order[i + 1]

    def handle_click(self):
        pos = pygame.mouse.get_pos()
        if self.ui.end_turn_button_rect.collidepoint(pos):
            self.end_turn()
        elif self.action_wheel_target:
            action_obj = self.action_wheel.handle_click(pos)
            if action_obj['val']:
                self.handle_action_wheel(action_obj)
            else:
                self.action_wheel_target = None
        else:
            if self.player.rect.collidepoint(pos):
                self.action_wheel.change_target(self.player)
                self.action_wheel_target = self.player.id
            else:
                for npc in self.npc_group:
                    if npc.rect.collidepoint(pos):
                        self.action_wheel.change_target(npc)
                        self.action_wheel_target = npc.id
