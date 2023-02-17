import pygame
from math import sin
from utils.settings import *


class Creature(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.frame = 0
        self.animation_speed = EFFECTS['animation_speed']
        self.direction = pygame.math.Vector2()

    def change_visibility(self):
        value = sin(pygame.time.get_ticks())
        return 255 if value >= 0 else 0

    def move(self, speed):
        if self.direction.magnitude() >= 1:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.process_collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.process_collision('vertical')
        self.rect.center = self.hitbox.center

    def process_collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.barrier_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.barrier_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
