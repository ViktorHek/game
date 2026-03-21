import pygame

def get_adjasent_cord(pos, dir=None):
    x, y = pos[0], pos[1]
    dic = {
        'right': [x + 1, y],
        'left': [x - 1, y],
        'down': [x, y + 1],
        'up': [x, y - 1]
    }
    if dir:
        return dic[dir]
    else:
        return dic

def get_key_text(key):
    text = ''
    if key == pygame.K_RIGHT:
        text = 'right'
    elif key == pygame.K_LEFT:
        text = 'left'
    elif key == pygame.K_DOWN:
        text = 'down'
    elif key == pygame.K_UP:
        text = 'up'
    else:
        print('key missing in utils/get_key_text')
    return text

def get_shadow_surf(img, scale=1.1, offset=2):
    w, h = img.get_width(), img.get_height()
    shadow = pygame.Surface((w * scale, h * scale), pygame.SRCALPHA).convert_alpha()
    while scale > 1:
        scaled_img = pygame.transform.scale(img, (w * scale, h * scale))
        shadow_mask = pygame.mask.from_surface(scaled_img).to_surface(setcolor=(0,0,0,3), unsetcolor=None)
        shadow.blit(shadow_mask, shadow_mask.get_rect(center = (w / 2 + offset, h / 2 + offset)))
        scale -= 0.01
    return shadow
