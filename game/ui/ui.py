import pygame
from utils.settings import *


class UserInterface:
    def __init__(self):
        self.display_surf = pygame.display.get_surface()
        self.font = pygame.font.Font(UI['font'], UI['fontsize'])

        self.hpbar_rect = pygame.Rect(10, 10, UI['hpbar_width'], UI['bar_height'])
        self.energybar_rect = pygame.Rect(10, 34, UI['energybar_width'], UI['bar_height'])

        self.sword_graphic = pygame.image.load(SWORD['graphic']).convert_alpha()
        self.spell_graphics = []
        for spell in SPELLS.values():
            spell = pygame.image.load(spell['graphic']).convert_alpha()
            self.spell_graphics.append(spell)

    def render_bar(self, actual, maximum, bg_rect, colour):
        pygame.draw.rect(self.display_surf, COLOURS['ui_bg'], bg_rect)

        ratio = actual / maximum
        actual_width = bg_rect.width * ratio
        actual_rect = bg_rect.copy()
        actual_rect.width = actual_width

        pygame.draw.rect(self.display_surf, colour, actual_rect)
        pygame.draw.rect(self.display_surf, COLOURS['ui_border'], bg_rect, 3)

    def render_experience(self, experience):
        text_surf = self.font.render(str(int(experience)), False, COLOURS['text'])
        x_coord = self.display_surf.get_size()[0] - 20
        y_coord = self.display_surf.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x_coord, y_coord))

        pygame.draw.rect(self.display_surf, COLOURS['ui_bg'], text_rect.inflate(20, 20))
        self.display_surf.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surf, COLOURS['ui_border'], text_rect.inflate(20, 20), 3)

    def select_weaponbox(self, left, top, is_switched=False):
        bg_rect = pygame.Rect(left, top, UI['weaponbox_size'], UI['weaponbox_size'])
        pygame.draw.rect(self.display_surf, COLOURS['ui_bg'], bg_rect)
        if is_switched:
            pygame.draw.rect(self.display_surf, COLOURS['ui_border_active'], bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surf, COLOURS['ui_border'], bg_rect, 3)
        return bg_rect

    def overlay_swordbox(self):
        bg_rect = self.select_weaponbox(10, self.display_surf.get_size()[1] - 90)
        sword_image = self.sword_graphic
        sword_rect = sword_image.get_rect(center=bg_rect.center)
        self.display_surf.blit(sword_image, sword_rect)

    def overlay_spellbox(self, spell, is_switched):
        bg_rect = self.select_weaponbox(80, self.display_surf.get_size()[1] - 85, is_switched)
        spell_image = self.spell_graphics[spell]
        spell_rect = spell_image.get_rect(center=bg_rect.center)
        self.display_surf.blit(spell_image, spell_rect)

    def render_alert(self, text, colour):
        alert_font = pygame.font.Font(UI['font'], UI['fontsize_alert'])
        alert_surf = alert_font.render(text, False, colour)
        x_coord = self.display_surf.get_size()[0] // 2
        y_coord = self.display_surf.get_size()[1] // 3
        alert_rect = alert_surf.get_rect(center=(x_coord, y_coord))

        pygame.draw.rect(self.display_surf, COLOURS['ui_bg'], alert_rect.inflate(20, 20))
        self.display_surf.blit(alert_surf, alert_rect)
        pygame.draw.rect(self.display_surf, COLOURS['ui_border'], alert_rect.inflate(20, 20), 3)

    def render(self, player):
        self.render_bar(player.hp, player.abilities['hp'], self.hpbar_rect, COLOURS['hp'])
        self.render_bar(player.energy, player.abilities['energy'], self.energybar_rect, COLOURS['energy'])
        self.render_experience(player.experience)
        self.overlay_swordbox()
        self.overlay_spellbox(player.spell, not player.can_switch_spell)
