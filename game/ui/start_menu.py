import pygame
from utils.settings import *
from level.level import *


class Button:
	def __init__(self, left, top, index, font):
		self.rect = pygame.Rect(left, top, START_MENU['btn_width'], START_MENU['btn_height'])
		self.index = index
		self.font = font

	def render_name(self, surf, name, is_selected):
		colour = COLOURS['text_active'] if is_selected else COLOURS['text']
		name_surf = self.font.render(name, False, colour)
		name_rect = name_surf.get_rect(center=self.rect.center)
		surf.blit(name_surf, name_rect)

	def render(self, surf, name, selection_index):
		if self.index == selection_index:
			pygame.draw.rect(surf, COLOURS['menu_bg_active'], self.rect)
		else:
			pygame.draw.rect(surf, COLOURS['ui_bg'], self.rect)
		pygame.draw.rect(surf, COLOURS['ui_border'], self.rect, 4)
		self.render_name(surf, name, self.index == selection_index)
		

class StartMenu:
	def __init__(self):
		self.btns = []
		self.is_game_started = False
		self.is_game_quit = False

		self.display_surf = pygame.display.get_surface()
		self.bg_surf = pygame.image.load(START_MENU['image']).convert_alpha()
		self.width = self.display_surf.get_size()[0]
		self.height = self.display_surf.get_size()[1]

		self.btn_names = [START_MENU['btn_play'], START_MENU['btn_quit']]
		self.btn_count = len(self.btn_names)
		self.font = pygame.font.Font(START_MENU['font'], START_MENU['fontsize'])

		self.selection_index = 0
		self.selection_time = None
		self.can_move = True

		self.render_btns()

		self.start_theme = pygame.mixer.Sound(START_MENU['audio'])
		self.start_theme.set_volume(SOUNDS_VOLUME['start_theme'])

	def process_input(self):
		keys = pygame.key.get_pressed()

		if not self.is_game_started:
			if self.can_move:
				if keys[pygame.K_SPACE]:
					self.can_move = False
					self.selection_time = pygame.time.get_ticks()

					if self.btn_names[self.selection_index] == START_MENU['btn_play']:
						self.is_game_started = True
					elif self.btn_names[self.selection_index] == START_MENU['btn_quit']:
						self.is_game_quit = True

				if keys[pygame.K_DOWN] and (self.selection_index < (self.btn_count - 1)):
					self.selection_index += 1
					self.can_move = False
					self.selection_time = pygame.time.get_ticks()
				elif keys[pygame.K_UP] and (self.selection_index >= 1):
					self.selection_index -= 1
					self.can_move = False
					self.selection_time = pygame.time.get_ticks()

	def cooldown_selection(self):
		if not self.can_move:
			actual_time = pygame.time.get_ticks()
			if (actual_time - self.selection_time) >= 300:
				self.can_move = True

	def render_btns(self):
		left = (self.width // 2) - (START_MENU['btn_width'] // 2)
		for factor, index in enumerate(range(self.btn_count)):
			top = (self.height * 0.4) + (factor * START_MENU['btn_offset'])
			btn = Button(left, top, index, self.font)
			self.btns.append(btn)

	def render(self):
		self.display_surf.blit(self.bg_surf, START_MENU['image_position'])
		self.process_input()
		self.cooldown_selection()
		for index, btn in enumerate(self.btns):
			btn.render(self.display_surf, self.btn_names[index], self.selection_index)
