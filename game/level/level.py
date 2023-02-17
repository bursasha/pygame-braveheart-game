import pygame
from ui.ability_menu import *
from ui.ui import *
from weapons.spell import *
from weapons.sword import *
from utils.support import *
from utils.settings import *
from creatures.player import *
from creatures.monster import *
from level.visual_effect import *
from level.tile import *


class Level:
    def __init__(self):
        self.is_quit = False
        self.is_paused = False
        self.is_boss_alive = True
        self.can_open_ability_menu = True
        self.can_quit = False

        self.player = None
        self.visible_sprites = VerticalCameraGroup()
        self.barrier_sprites = pygame.sprite.Group()

        self.actual_attack = None
        self.attacking_sprites = pygame.sprite.Group()
        self.attacked_sprites = pygame.sprite.Group()

        self.selection_time = None

        self.render_map()
        self.ui = UserInterface()
        self.ability_menu = AbilityMenu(self.player)
        self.visual_effect = VisualEffect()
        self.spell = Spell(self.visual_effect)

        self.main_theme = pygame.mixer.Sound(MAP['audio'])
        self.main_theme.set_volume(SOUNDS_VOLUME['main_theme'])

    def render_map(self):
        layouts = {
            'boundaries': import_layout(MAP['layouts']['boundaries']),
            'small_objects': import_layout(MAP['layouts']['small_objects']),
            'medium_objects': import_layout(MAP['layouts']['medium_objects']),
            'large_objects': import_layout(MAP['layouts']['large_objects']),
            'creatures': import_layout(MAP['layouts']['creatures'])
        }
        graphics = {
            'small_objects': import_assets(MAP['graphics']['small_objects']),
            'medium_objects': import_assets(MAP['graphics']['medium_objects']),
            'large_objects': import_assets(MAP['graphics']['large_objects'])
        }

        for sprite_type, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for column_index, column in enumerate(row):
                    if column != MAP['layouts']['empty_tile']:
                        x_coord = column_index * GAME_SETUP['tilesize']
                        y_coord = row_index * GAME_SETUP['tilesize']

                        if sprite_type == 'boundaries':
                            Tile((x_coord, y_coord), [self.barrier_sprites], 'invisible')

                        if sprite_type == 'small_objects' or sprite_type == 'medium_objects' or \
                                sprite_type == 'large_objects':
                            image_surf = graphics[sprite_type][int(column)]
                            Tile((x_coord, y_coord), [self.barrier_sprites, self.visible_sprites], sprite_type,
                                 image_surf)

                        if sprite_type == 'creatures':
                            if column == MAP['layouts']['player_tile']:
                                self.player = Player((x_coord, y_coord), [self.visible_sprites], self.barrier_sprites,
                                                     self.start_attack, self.end_attack, self.process_spell)
                            else:
                                monster_name = MAP['layouts']['monster_tiles'][column]
                                Monster(monster_name, (x_coord, y_coord), [self.visible_sprites, self.attacked_sprites],
                                        self.barrier_sprites, self.player_get_damage, self.player_get_experience,
                                        self.render_death_effect)

    def start_attack(self):
        self.actual_attack = Sword(self.player, [self.visible_sprites, self.attacking_sprites])

    def end_attack(self):
        if self.actual_attack:
            self.actual_attack.kill()
        self.actual_attack = None

    def process_spell(self, spell, power, worth):
        if spell == 'heal':
            self.spell.heal(self.player, [self.visible_sprites], power, worth)
        if spell == 'fireball':
            self.spell.fireball(self.player, [self.visible_sprites, self.attacking_sprites], worth)

    def player_attack_logic(self):
        if self.attacking_sprites:
            for attacking_sprite in self.attacking_sprites:
                collided_sprites = pygame.sprite.spritecollide(attacking_sprite, self.attacked_sprites, False)
                if collided_sprites:
                    for collided_sprite in collided_sprites:
                        collided_sprite.get_damage(self.player, attacking_sprite.sprite_type)

    def player_get_damage(self, damage, attack_type):
        if self.player.is_vulnerable:
            self.player.is_vulnerable = False
            self.player.hp -= damage
            self.player.hurt_time = pygame.time.get_ticks()
            self.visual_effect.render([self.visible_sprites], attack_type, self.player.rect.center)

    def control_quit(self):
        self.is_boss_alive = [True for sprite in self.attacked_sprites if sprite.name == MONSTERS['boss']]
        if self.player.is_dead or not self.is_boss_alive:
            self.selection_time = pygame.time.get_ticks()
            self.can_quit = True

    def quit(self):
        if self.player.is_dead:
            self.ui.render_alert(UI['alert_lose'], COLOURS['alert_lose'])
        else:
            self.ui.render_alert(UI['alert_victory'], COLOURS['alert_victory'])

        actual_time = pygame.time.get_ticks()
        if (actual_time - self.selection_time) >= 3000:
            self.is_quit = True
            self.can_quit = False
            self.selection_time = None
            self.clear_map()
            self.render_map()

    def clear_map(self):
        [sprite.kill() for sprite in self.barrier_sprites]
        [sprite.kill() for sprite in self.visible_sprites]
        [sprite.kill() for sprite in self.attacking_sprites]
        [sprite.kill() for sprite in self.attacked_sprites]

    def player_get_experience(self, amount):
        self.player.experience += amount

    def render_death_effect(self, position, particle):
        self.visual_effect.render(self.visible_sprites, particle, position)

    def control_ability_menu(self):
        keys = pygame.key.get_pressed()
        if self.can_open_ability_menu:
            if keys[pygame.K_m]:
                self.selection_time = pygame.time.get_ticks()
                self.is_paused = not self.is_paused
                self.can_open_ability_menu = False

    def cooldown_selection(self):
        if not self.can_open_ability_menu:
            actual_time = pygame.time.get_ticks()
            if (actual_time - self.selection_time) >= 300:
                self.selection_time = None
                self.can_open_ability_menu = True

    def render(self):
        self.visible_sprites.render_camera(self.player)
        self.ui.render(self.player)
        self.control_ability_menu()
        self.cooldown_selection()

        if self.is_paused:
            self.ability_menu.render()
        else:
            if self.can_quit:
                self.quit()
            else:
                self.visible_sprites.update()
                self.visible_sprites.render_monsters(self.player)
                self.player_attack_logic()
                self.control_quit()


class VerticalCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.half_width = self.display_surf.get_size()[0] // 2
        self.half_height = self.display_surf.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.bg_surf = pygame.image.load(MAP['graphics']['map']).convert()
        self.bg_rect = self.bg_surf.get_rect(topleft=(0, 0))

    def render_camera(self, player):
        self.display_surf.fill(COLOURS['water'])

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        ground_offset_position = self.bg_rect.topleft - self.offset
        self.display_surf.blit(self.bg_surf, ground_offset_position)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surf.blit(sprite.image, offset_position)

    def render_monsters(self, player):
        monster_sprites = [sprite for sprite in self.sprites() if
                           hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'monster']
        for monster in monster_sprites:
            monster.render(player)
