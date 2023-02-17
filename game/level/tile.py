import pygame
from utils.settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, position, sprite_groups, sprite_type,
                 surf=pygame.Surface((GAME_SETUP['tilesize'], GAME_SETUP['tilesize']))):
        super().__init__(sprite_groups)
        self.sprite_type = sprite_type
        self.image = surf
        self.rect = self.image.get_rect(topleft=position)

        if sprite_type == 'large_objects':
            self.hitbox = self.rect.inflate(0, -10 - (2 * GAME_SETUP['tilesize']))
        elif sprite_type == 'medium_objects':
            self.hitbox = self.rect.inflate(0, -10 - GAME_SETUP['tilesize'])
        else:
            self.hitbox = self.rect.inflate(0, -10)
