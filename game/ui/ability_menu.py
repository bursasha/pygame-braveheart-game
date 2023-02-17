import pygame
from utils.settings import *


class AbilityBar:
    def __init__(self, left, top, width, height, index, font):
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font

    def render_name(self, surf, name, worth, is_selected):
        colour = COLOURS['text_active'] if is_selected else COLOURS['text']
        name_surf = self.font.render(name, False, colour)
        name_rect = name_surf.get_rect(midtop=(self.rect.midtop + pygame.math.Vector2(0, 20)))
        worth_surf = self.font.render(f'{int(worth)}', False, colour)
        worth_rect = worth_surf.get_rect(midbottom=(self.rect.midbottom - pygame.math.Vector2(0, 20)))

        surf.blit(name_surf, name_rect)
        surf.blit(worth_surf, worth_rect)

    def render_bar(self, surf, actual, maximum, is_selected):
        colour = COLOURS['ability_bar_active'] if is_selected else COLOURS['ability_bar']
        top = (self.rect.midtop + pygame.math.Vector2(0, 60))
        bottom = (self.rect.midbottom - pygame.math.Vector2(0, 60))
        bar_height = bottom[1] - top[1]
        actual_height = (actual / maximum) * bar_height
        actual_rect = pygame.Rect(top[0] - 15, bottom[1] - actual_height, 30, 10)

        pygame.draw.line(surf, colour, top, bottom, 5)
        pygame.draw.rect(surf, colour, actual_rect)

    def upgrade(self, player):
        ability = list(player.abilities.keys())[self.index]

        if player.experience >= player.upgrade_worth[ability] and \
                player.abilities[ability] < player.max_abilities[ability]:
            player.experience -= player.upgrade_worth[ability]
            player.abilities[ability] *= UPGRADES['ability_factor']
            player.upgrade_worth[ability] *= UPGRADES['worth_factor']

        if player.abilities[ability] > player.max_abilities[ability]:
            player.abilities[ability] = player.max_abilities[ability]

    def render(self, surf, selection_index, name, actual, maximum, worth):
        if self.index == selection_index:
            pygame.draw.rect(surf, COLOURS['menu_bg_active'], self.rect)
            pygame.draw.rect(surf, COLOURS['ui_border'], self.rect, 4)
        else:
            pygame.draw.rect(surf, COLOURS['ui_bg'], self.rect)
            pygame.draw.rect(surf, COLOURS['ui_border'], self.rect, 4)

        self.render_name(surf, name, worth, self.index == selection_index)
        self.render_bar(surf, actual, maximum, self.index == selection_index)


class AbilityMenu:
    def __init__(self, player):
        self.abilities = []
        self.display_surf = pygame.display.get_surface()
        self.player = player
        self.ability_count = len(player.abilities)
        self.ability_names = list(player.abilities.keys())
        self.maximums = list(player.max_abilities.values())
        self.font = pygame.font.Font(UI['font'], UI['fontsize'])

        self.width = self.display_surf.get_size()[0] // (self.ability_count + 1)
        self.height = self.display_surf.get_size()[1] * 0.75
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

        self.render_ability_bars()

    def process_input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.abilities[self.selection_index].upgrade(self.player)

            if keys[pygame.K_LEFT] and (self.selection_index >= 1):
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_RIGHT] and ((self.ability_count - 1) > self.selection_index):
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

    def cooldown_selection(self):
        if not self.can_move:
            actual_time = pygame.time.get_ticks()
            if (actual_time - self.selection_time) >= 300:
                self.can_move = True

    def render_ability_bars(self):
        menu_width = self.display_surf.get_size()[0]
        offset = menu_width // self.ability_count

        for factor, index in enumerate(range(self.ability_count)):
            left = (factor * offset) + (offset - self.width) // 2
            top = self.display_surf.get_size()[1] * 0.1
            ability = AbilityBar(left, top, self.width, self.height, index, self.font)
            self.abilities.append(ability)

    def render(self):
        self.process_input()
        self.cooldown_selection()

        for index, ability in enumerate(self.abilities):
            name = self.ability_names[index]
            actual = self.player.get_ability_by_index(index)
            maximum = self.maximums[index]
            worth = self.player.get_worth_by_index(index)
            ability.render(self.display_surf, self.selection_index, name, actual, maximum, worth)
