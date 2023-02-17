import pygame
from utils.settings import *
from utils.support import *
from creatures.creature import *


class Player(Creature):
    def __init__(self, position, sprite_groups, barrier_sprites, start_attack, end_attack, process_spell):
        super().__init__(sprite_groups)

        self.is_dead = False

        self.image = pygame.image.load(PLAYER['graphic'])
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(PLAYER['hitbox_offset'])

        self.graphics = None
        self.import_graphics()
        self.status = PLAYER_STATUSES['D']

        self.is_attacking = False
        self.attack_cooldown = PLAYER['attack_cooldown']
        self.attack_time = None

        self.start_attack = start_attack
        self.end_attack = end_attack
        self.process_spell = process_spell
        self.barrier_sprites = barrier_sprites

        self.spell = 0
        self.spells = list(SPELLS.keys())
        self.can_switch_spell = True
        self.spell_switch_time = None
        self.spell_switch_cooldown = PLAYER['spell_switch_cooldown']

        self.abilities = PLAYER['abilities']
        self.max_abilities = PLAYER['max_abilities']
        self.upgrade_worth = PLAYER['upgrade_worth']

        self.hp = self.abilities['hp'] * GAME_SETUP['start_hp_ratio']
        self.energy = self.abilities['energy'] * GAME_SETUP['start_energy_ratio']
        self.speed = self.abilities['speed']
        self.experience = GAME_SETUP['start_experience']

        self.is_vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = PLAYER['invulnerability_duration']

        self.sword_sound = pygame.mixer.Sound(SWORD['sound'])
        self.sword_sound.set_volume(SOUNDS_VOLUME['sword_attack'])

    def import_graphics(self):
        self.graphics = {
            PLAYER_STATUSES['U']: [],
            PLAYER_STATUSES['D']: [],
            PLAYER_STATUSES['L']: [],
            PLAYER_STATUSES['R']: [],

            PLAYER_STATUSES['UI']: [],
            PLAYER_STATUSES['DI']: [],
            PLAYER_STATUSES['LI']: [],
            PLAYER_STATUSES['RI']: [],

            PLAYER_STATUSES['UA']: [],
            PLAYER_STATUSES['DA']: [],
            PLAYER_STATUSES['LA']: [],
            PLAYER_STATUSES['RA']: []
        }

        for status in self.graphics.keys():
            graphic_path = PLAYER['path'] + status
            self.graphics[status] = import_assets(graphic_path)

    def process_input(self):
        if not self.is_attacking:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = PLAYER_STATUSES['U']
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = PLAYER_STATUSES['D']
            else:
                self.direction.y = 0

            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = PLAYER_STATUSES['L']
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = PLAYER_STATUSES['R']
            else:
                self.direction.x = 0

            if keys[pygame.K_a]:
                self.is_attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.start_attack()
                self.sword_sound.play()

            if keys[pygame.K_s]:
                self.is_attacking = True
                self.attack_time = pygame.time.get_ticks()
                spell = self.spells[self.spell]
                power = list(SPELLS.values())[self.spell]['power'] + self.abilities['spell']
                worth = list(SPELLS.values())[self.spell]['worth']
                self.process_spell(spell, power, worth)

            if keys[pygame.K_w] and self.can_switch_spell:
                self.can_switch_spell = False
                self.spell_switch_time = pygame.time.get_ticks()

                if self.spell < len(self.spells) - 1:
                    self.spell += 1
                else:
                    self.spell = 0

    def process_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not ('idle' in self.status or 'attack' in self.status):
                self.status += '_idle'

        if self.is_attacking:
            self.direction.x = 0
            self.direction.y = 0
            if 'attack' not in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status += '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def animate(self):
        animation = self.graphics[self.status]
        self.frame += self.animation_speed
        if self.frame >= len(animation):
            self.frame = 0

        self.image = animation[int(self.frame)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.is_vulnerable:
            alpha = self.change_visibility()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldown_attack(self):
        actual_time = pygame.time.get_ticks()

        if self.is_attacking:
            if (actual_time - self.attack_time) >= (self.attack_cooldown + SWORD['cooldown']):
                self.is_attacking = False
                self.end_attack()
        if not self.can_switch_spell:
            if (actual_time - self.spell_switch_time) >= self.spell_switch_cooldown:
                self.can_switch_spell = True

        if not self.is_vulnerable:
            if (actual_time - self.hurt_time) >= self.invulnerability_duration:
                self.is_vulnerable = True

    def attack_sword(self):
        return self.abilities['attack'] + SWORD['damage']

    def cast_spell(self):
        return self.abilities['spell'] + SPELLS['fireball']['power']

    def control_death(self):
        if self.hp <= 0:
            self.is_dead = True

    def get_ability_by_index(self, index):
        return list(self.abilities.values())[index]

    def get_worth_by_index(self, index):
        return list(self.upgrade_worth.values())[index]

    def energy_regeneration(self):
        if self.energy < self.abilities['energy']:
            self.energy += (PLAYER['energy_regeneration_factor'] * self.abilities['spell'])
        else:
            self.energy = self.abilities['energy']

    def update(self):
        self.process_input()
        self.cooldown_attack()
        self.process_status()
        self.animate()
        self.move(self.abilities['speed'])
        self.energy_regeneration()
        self.control_death()
