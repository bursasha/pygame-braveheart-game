import pygame
from utils.settings import *
from utils.support import *
from creatures.creature import *


class Monster(Creature):
    def __init__(self, name, position, sprite_groups, barrier_sprites, player_get_damage, player_get_experience,
                 render_death_effect):
        super().__init__(sprite_groups)
        self.sprite_type = 'monster'

        self.graphics = None
        self.import_graphics(name)
        self.status = MONSTER_STATUSES['I']
        self.image = self.graphics[self.status][self.frame]

        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(MONSTERS[name]['hitbox_offset'])
        self.barrier_sprites = barrier_sprites

        self.name = name
        self.hp = MONSTERS[name]['hp']
        self.damage = MONSTERS[name]['damage']
        self.experience = MONSTERS[name]['experience']
        self.speed = MONSTERS[name]['speed']
        self.resistance = MONSTERS[name]['resistance']
        self.attack_radius = MONSTERS[name]['attack_radius']
        self.notice_radius = MONSTERS[name]['notice_radius']
        self.attack_type = MONSTERS[name]['attack_type']

        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = MONSTERS[name]['attack_cooldown']
        self.is_vulnerable = True
        self.hit_time = None
        self.invulnerability_duration = MONSTERS[name]['invulnerability_duration']

        self.player_get_damage = player_get_damage
        self.player_get_experience = player_get_experience
        self.render_death_effect = render_death_effect

        self.hit_sound = pygame.mixer.Sound(MONSTERS[name]['hit_sound'])
        self.attack_sound = pygame.mixer.Sound(MONSTERS[name]['attack_sound'])
        self.death_sound = pygame.mixer.Sound(MONSTERS[name]['death_sound'])
        self.hit_sound.set_volume(SOUNDS_VOLUME['monster_hit'])
        self.attack_sound.set_volume(SOUNDS_VOLUME['monster_attack'])
        self.death_sound.set_volume(SOUNDS_VOLUME['monster_death'])

    def import_graphics(self, name):
        self.graphics = {MONSTER_STATUSES['I']: [], MONSTER_STATUSES['M']: [], MONSTER_STATUSES['A']: []}
        graphic_path = MONSTERS['path'] + name + '/'
        for status in self.graphics.keys():
            self.graphics[status] = import_assets(graphic_path + status)

    def get_player_position(self, player):
        monster_position = pygame.math.Vector2(self.rect.center)
        player_position = pygame.math.Vector2(player.rect.center)
        distance = (player_position - monster_position).magnitude()
        if distance > 0:
            direction = (player_position - monster_position).normalize()
        else:
            direction = pygame.math.Vector2()

        return distance, direction

    def process_status(self, player):
        distance = self.get_player_position(player)[0]
        if distance <= self.attack_radius and self.can_attack:
            if self.status != MONSTER_STATUSES['A']:
                self.frame = 0
            self.status = MONSTER_STATUSES['A']
        elif distance <= self.notice_radius:
            self.status = MONSTER_STATUSES['M']
        else:
            self.status = MONSTER_STATUSES['I']

    def process_action(self, player):
        if self.status == MONSTER_STATUSES['A']:
            self.attack_time = pygame.time.get_ticks()
            self.player_get_damage(self.damage, self.attack_type)
            self.attack_sound.play()
        elif self.status == MONSTER_STATUSES['M']:
            self.direction = self.get_player_position(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.graphics[self.status]
        self.frame += self.animation_speed

        if self.frame >= len(animation):
            if self.status == MONSTER_STATUSES['A']:
                self.can_attack = False
            self.frame = 0

        self.image = animation[int(self.frame)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.is_vulnerable:
            self.image.set_alpha(self.change_visibility())
        else:
            self.image.set_alpha(255)

    def cooldown_attack(self):
        actual_time = pygame.time.get_ticks()
        if not self.can_attack:
            if (actual_time - self.attack_time) >= self.attack_cooldown:
                self.can_attack = True

        if not self.is_vulnerable:
            if (actual_time - self.hit_time) >= self.invulnerability_duration:
                self.is_vulnerable = True

    def get_damage(self, player, attack_type):
        if self.is_vulnerable:
            self.hit_sound.play()
            self.direction = self.get_player_position(player)[1]

            if attack_type == 'sword':
                self.hp -= player.attack_sword()
            else:
                self.hp -= player.cast_spell()
            self.hit_time = pygame.time.get_ticks()
            self.is_vulnerable = False

    def control_death(self):
        if self.hp <= 0:
            self.render_death_effect(self.rect.center, self.name)
            self.kill()
            self.player_get_experience(self.experience)
            self.death_sound.play()

    def react_to_attack(self):
        if not self.is_vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.react_to_attack()
        self.move(self.speed)
        self.animate()
        self.cooldown_attack()
        self.control_death()

    def render(self, player):
        self.process_status(player)
        self.process_action(player)
