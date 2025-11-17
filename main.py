import sys
import pygame

from pytmx.util_pygame import load_pygame

class Player():
    def __init__(self, game):
        self.player_size = 16
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load('assets/test_char.bmp'), (16,16))
        self.rect = self.image.get_rect()
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.rect.x = 16
        self.rect.y = 16
        self.speed = 1
        self.inventory = []
    
    def blitme(self):
        self.game.screen.blit(self.image, self.rect)
    
    def update(self):
        if self.moving_right:
            self.rect.x += self.speed
        if self.moving_left:
            self.rect.x -= self.speed
        if self.moving_down:
            self.rect.y += self.speed
        if self.moving_up:
            self.rect.y -= self.speed

class Main():
    def __init__(self):
        pygame.init()
        self.screen_width = 800 # 800 / 16 = 50
        self.screen_height = 480 # 480 / 16 = 30
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        self.tile_size = 16
        self.base_tile_prop = {
            'id': -1, 'collide': 0, 'source': '', 'trans': None, 'width': '16', 'height': '16', 'frames': []
        }
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Akavir: God of none')
        self.tmxdata = load_pygame('map/test_map.tmx')
        self.counter = 0
        self.amount_of_layers = 2
        self.game_is_running = True
        self.player = Player(self)

    def run(self):
        while self.game_is_running:
            self.check_event()
            self.update_player2()
            self.clock.tick(60)
            self.update_screen()

    def check_tile(self, x, y, dir=None, layer=1):
        size = self.tile_size
        x = (x + size // 2) // size
        y = (y + size // 2) // size
        if dir == None:
            return self.try_get_prop(x, y, layer)
        elif dir == 'right':
            x = (x + 4 + size // 2)
        elif dir == 'left':
            x = (x + 4) // size
        elif dir == 'up':
            y = (y + 4) // size
        elif dir == 'down':
            (y + 4 + size // 2) // size

        return self.try_get_prop(x, y, layer)

    def update_player(self):
        x = self.player.rect.x
        y = self.player.rect.y
        layer = 1
        can_move_right = True
        can_move_left = True
        can_move_up = True
        can_move_down = True 
        can_move_right = self.check_tile(x, y, 'right', layer)['collide'] == 1
        can_move_left = self.check_tile(x, y, 'left', layer)['collide'] == 1
        can_move_up = self.check_tile(x, y, 'up', layer)['collide'] == 1
        can_move_down = self.check_tile(x, y, 'down', layer)['collide'] == 1
        if self.player.moving_right:
            self.player.moving_right = not can_move_right
        if self.player.moving_left:
            self.player.moving_left = not can_move_left
        if self.player.moving_up:
            self.player.moving_up = not can_move_up
        if self.player.moving_down:
            self.player.moving_down = not can_move_down
        self.player.update()


    def update_player2(self):
        x = self.player.rect.x
        y = self.player.rect.y
        size = self.tile_size
        layer = 1
        right_pos = (
            (x + 4 + size // 2) // size,
            (y + size // 2) // size
        )
        left_pos = (
            (x + 4) // size,
            (y + size // 2) // size
        )
        top_pos = (
            (x + size // 2) // size,
            (y + 4) // size
        )
        bottom_pos = (
            (x + size // 2) // size,
            (y + 4 + size // 2) // size
        )
        right_tile = self.try_get_prop(right_pos[0], right_pos[1], layer)
        left_tile = self.try_get_prop(left_pos[0], left_pos[1], layer)
        top_tile = self.try_get_prop(top_pos[0], top_pos[1], layer)
        bottom_tile = self.try_get_prop(bottom_pos[0], bottom_pos[1], layer)
        
        if right_tile['collide'] == 1:
            self.player.moving_right = False
        if left_tile['collide'] == 1:
            self.player.moving_left = False
        if top_tile['collide'] == 1:
            self.player.moving_up = False
        if bottom_tile['collide'] == 1:
            self.player.moving_down = False
        self.player.update()

    def get_surrounding_tiles(self):
        x = (self.player.rect.x + self.player.player_size / 2) // self.player.player_size
        y = (self.player.rect.y + self.player.player_size / 2) // self.player.player_size
        # x = self.player.rect.x // self.player.player_size
        # y = self.player.rect.y // self.player.player_size
        arr = []
        for i in range(self.amount_of_layers):
            tile_grid = {
                'top_left': self.try_get_prop(x-1, y-1, i),
                'top': self.try_get_prop(x, y-1, i),
                'top_right': self.try_get_prop(x+1, y-1, i),
                'left': self.try_get_prop(x-1, y, i),
                'center': self.try_get_prop(x, y, i),
                'right': self.try_get_prop(x+1, y, i),
                'bottom_left': self.try_get_prop(x-1, y+1, i),
                'bottom': self.try_get_prop(x, y+1, i),
                'bottom_right': self.try_get_prop(x+1, y+1, i),
            }
            arr.append(tile_grid)
        return arr

    def try_get_prop(self, x, y, layer=0):
        try:
            properties = self.tmxdata.get_tile_properties(x, y, layer)
        except ValueError:
            properties = self.base_tile_prop
        if properties is None:
            properties = self.base_tile_prop
        # return properties['collide']
        return properties

    def update_screen(self):
        self.screen.fill((100,100,100))
        self.blit_all_tiles(self.tmxdata)
        # self.player.blitme()
        pygame.display.flip()

    def blit_all_tiles(self, tmxdata):
        for i, layer in enumerate(tmxdata):
            if i == 0:
                self.blit_map_tile(layer, i)
            elif i == 1:
                self.blit_map_tile(layer, i)
            # elif i == 2:
            #     if self.counter > 30:
            #         self.blit_map_tile(layer)
        self.counter = self.counter + 1 if self.counter < 60 else 0

    def blit_map_tile(self, layer, index):
        for tile in layer.tiles():
            x_pixel = tile[0] * 16
            y_pixel = tile[1] * 16
            self.screen.blit(tile[2], (x_pixel, y_pixel))
            if y_pixel >= self.player.rect.y:
                self.player.blitme() 
            if y_pixel <= self.player.rect.y:
                self.screen.blit(tile[2], (x_pixel, y_pixel))
                
    def check_event(self):
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            self.player.moving_down = keys[pygame.K_DOWN]
            self.player.moving_up = keys[pygame.K_UP]
            self.player.moving_right = keys[pygame.K_RIGHT]
            self.player.moving_left = keys[pygame.K_LEFT]
            if event.type == pygame.QUIT:
                sys.exit()
            

if __name__ == '__main__':
    game = Main()
    game.run()
