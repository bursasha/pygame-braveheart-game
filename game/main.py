import pygame
import sys
import pyautogui
from utils.settings import *
from ui.start_menu import *
from level.level import *


class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((GAME_SETUP['width'], GAME_SETUP['height']))
		pygame.display.set_caption(GAME_SETUP['gamename'])
		self.clock = pygame.time.Clock()
		self.start_menu = StartMenu()
		self.level = Level()

	def render(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			if not self.start_menu.is_game_started:
				self.level.main_theme.stop()
				self.start_menu.render()
				self.start_menu.start_theme.play(-1)

				if self.start_menu.is_game_quit:
					pygame.quit()
					sys.exit()
			else:
				self.start_menu.start_theme.stop()
				self.level.render()
				self.level.main_theme.play(-1)

				if self.level.is_quit:
					self.start_menu.is_game_started = False
					self.level.is_quit = False
					self.level.is_boss_alive = True

			pygame.display.update()
			self.clock.tick(GAME_SETUP['fps'])


if __name__ == '__main__':
	BraveHeart = Game()
	BraveHeart.render()
