import pygame
from random import randint
from utils.settings import *


class Spell:
	def __init__(self, visual_effect):
		self.visual_effect = visual_effect
		self.sounds = {
			'heal': pygame.mixer.Sound(SPELLS['heal']['sound']),
			'fireball': pygame.mixer.Sound(SPELLS['fireball']['sound'])
		}

	def heal(self, player, sprite_groups, power, worth):
		if player.energy >= worth:
			self.sounds['heal'].set_volume(SOUNDS_VOLUME['spells'])
			self.sounds['heal'].play()
			player.hp += power
			player.energy -= worth

			if player.hp >= player.abilities['hp']:
				player.hp = player.abilities['hp']

			self.visual_effect.render(sprite_groups, 'heal', player.rect.center)

	def fireball(self, player, sprite_groups, worth):
		if player.energy >= worth:
			self.sounds['fireball'].set_volume(SOUNDS_VOLUME['spells'])
			self.sounds['fireball'].play()
			player.energy -= worth

			player_direction = player.status.split('_')[0]
			if player_direction == DIRECTIONS['R']:
				flame_direction = pygame.math.Vector2(1, 0)
			elif player_direction == DIRECTIONS['L']:
				flame_direction = pygame.math.Vector2(-1, 0)
			elif player_direction == DIRECTIONS['U']:
				flame_direction = pygame.math.Vector2(0, -1)
			else:
				flame_direction = pygame.math.Vector2(0, 1)

			for fireball_number in range(1, 4):
				if flame_direction.x:
					offset = (flame_direction.x * fireball_number) * GAME_SETUP['tilesize']
					x = player.rect.centerx + offset + \
						randint(-GAME_SETUP['tilesize'] // 3, GAME_SETUP['tilesize'] // 3)
					y = player.rect.centery + randint(-GAME_SETUP['tilesize'] // 3, GAME_SETUP['tilesize'] // 3)
					self.visual_effect.render(sprite_groups, 'fireball', (x, y))
				else:
					offset = (flame_direction.y * fireball_number) * GAME_SETUP['tilesize']
					x = player.rect.centerx + randint(-GAME_SETUP['tilesize'] // 3, GAME_SETUP['tilesize'] // 3)
					y = player.rect.centery + offset + \
						randint(-GAME_SETUP['tilesize'] // 3, GAME_SETUP['tilesize'] // 3)
					self.visual_effect.render(sprite_groups, 'fireball', (x, y))
