import pygame
from utils.settings import *


class Sword(pygame.sprite.Sprite):
	def __init__(self, player, sprite_groups):
		super().__init__(sprite_groups)

		self.sprite_type = 'sword'

		direction = player.status.split('_')[0]
		frame_path = SWORD['path'] + direction + '.png'
		self.image = pygame.image.load(frame_path).convert_alpha()

		if direction == DIRECTIONS['R']:
			self.rect = self.image.get_rect(midleft=(player.rect.midright + pygame.math.Vector2(0, 16)))
		elif direction == DIRECTIONS['L']:
			self.rect = self.image.get_rect(midright=(player.rect.midleft + pygame.math.Vector2(0, 16)))
		elif direction == DIRECTIONS['U']:
			self.rect = self.image.get_rect(midbottom=(player.rect.midtop + pygame.math.Vector2(-10, 0)))
		else:
			self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0))
