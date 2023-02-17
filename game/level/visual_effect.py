import pygame
from utils.support import import_assets
from utils.settings import *


class Particle(pygame.sprite.Sprite):
    def __init__(self, position, image_frames, sprite_groups):
        super().__init__(sprite_groups)

        self.sprite_type = 'spell'
        self.frame = 0
        self.animation_speed = EFFECTS['animation_speed']
        self.image_frames = image_frames
        self.image = self.image_frames[self.frame]
        self.rect = self.image.get_rect(center=position)

    def animate(self):
        self.frame += self.animation_speed
        if self.frame >= len(self.image_frames):
            self.kill()
        else:
            self.image = self.image_frames[int(self.frame)]

    def update(self):
        self.animate()


class VisualEffect:
    def __init__(self):
        self.effects = {
            # spells
            'fireball': import_assets(EFFECTS['fireball']),
            'heal': import_assets(EFFECTS['heal']),

            # attacks
            'claws': import_assets(EFFECTS['claws']),
            'slash': import_assets(EFFECTS['slash']),
            'leafs': import_assets(EFFECTS['leafs']),
            'thunder': import_assets(EFFECTS['thunder']),

            # monster deaths
            'frog': import_assets(EFFECTS['frog']),
            'cyclope': import_assets(EFFECTS['cyclope']),
            'leszy': import_assets(EFFECTS['leszy']),
            'raccoon': import_assets(EFFECTS['raccoon'])
        }

    def render(self, sprite_groups, attack_type, position):
        Particle(position, self.effects[attack_type], sprite_groups)
