GAME_SETUP = {
    'width': 1280,
    'height': 720,
    'fps': 60,
    'tilesize': 64,
    'startposition': (940, 2570),
    'gamename': 'Brave Heart',

    'start_hp_ratio': 0.75,
    'start_energy_ratio': 0.5,
    'start_experience': 0
}

START_MENU = {
    'btn_width': 200,
    'btn_height': 78,
    'btn_offset': 100,

    'btn_play': 'Play',
    'btn_quit': 'Quit',

    'fontsize': 30,
    'font': './graphics/font/font.ttf',

    'audio': './audio/start/start_theme.ogg',
    'image': './graphics/map/start.png',

    'image_position': (-100, -150)
}

COLOURS = {
    'hp': 'red',
    'energy': 'blue',
    'water': '#71DDEE',

    'ui_bg': '#222222',
    'ui_border': '#111111',
    'ui_border_active': 'gold',

    'text': '#EEEEEE',
    'text_active': '#111111',

    'ability_bar': '#EEEEEE',
    'ability_bar_active': '#111111',
    'menu_bg_active': '#EEEEEE',

    'alert_victory': '#80FF00',
    'alert_lose': '#FF3333'
}

UI = {
    'bar_height': 20,
    'hpbar_width': 200,
    'energybar_width': 140,
    'weaponbox_size': 80,

    'font': './graphics/font/font.ttf',
    'fontsize': 18,
    'fontsize_alert': 30,

    'alert_victory': 'That is victory!',
    'alert_lose': 'Game over'
}

SOUNDS_VOLUME = {
    'start_theme': 0.1,
    'main_theme': 0.1,

    'spells': 1,
    'sword_attack': 1,

    'monster_hit': 1,
    'monster_attack': 1,
    'monster_death': 1,

}

MAP = {
    'layouts': {
        'boundaries': './layouts/boundaries.csv',
        'small_objects': './layouts/small_objects.csv',
        'medium_objects': './layouts/medium_objects.csv',
        'large_objects': './layouts/large_objects.csv',
        'creatures': './layouts/creatures.csv',

        'empty_tile': '-1',
        'player_tile': '3',
        'monster_tiles': {
            '0': 'raccoon',
            '1': 'leszy',
            '2': 'cyclope',
            '4': 'frog'
        },
    },

    'graphics': {
        'small_objects': './graphics/small_objects',
        'medium_objects': './graphics/medium_objects',
        'large_objects': './graphics/large_objects',
        'map': './graphics/map/map.png'
    },

    'audio': './audio/main/main_theme.ogg'
}

PLAYER = {
    'abilities': {
        'hp': 100,
        'energy': 60,
        'attack': 8,
        'spell': 4,
        'speed': 5
    },
    'max_abilities': {
        'hp': 300,
        'energy': 180,
        'attack': 20,
        'spell': 10,
        'speed': 8
    },
    'upgrade_worth': {
        'hp': 100,
        'energy': 100,
        'attack': 100,
        'spell': 100,
        'speed': 100
    },

    'graphic': './graphics/player/down/down_0.png',
    'path': './graphics/player/',

    'energy_regeneration_factor': 0.005,
    'hitbox_offset': (-10, -30),
    'spell_switch_cooldown': 500,
    'attack_cooldown': 350,
    'invulnerability_duration': 1000
}

UPGRADES = {
    'ability_factor': 1.2,
    'worth_factor': 1.2
}

EFFECTS = {
    'fireball': './graphics/spells/fireball/frames',
    'heal': './graphics/spells/heal/frames',

    'claws': './graphics/particles/attacks/claws',
    'slash': './graphics/particles/attacks/slash',
    'leafs': './graphics/particles/attacks/leafs',
    'thunder': './graphics/particles/attacks/thunder',

    'frog': './graphics/particles/deaths/frog',
    'cyclope': './graphics/particles/deaths/cyclope',
    'leszy': './graphics/particles/deaths/leszy',
    'raccoon': './graphics/particles/deaths/raccoon',

    'animation_speed': 0.15
}

DIRECTIONS = {
    'R': 'right',
    'L': 'left',
    'U': 'up',
    'D': 'down'
}

SWORD = {
    'damage': 15,
    'cooldown': 100,
    'sound': './audio/fight/sword.wav',
    'path': './graphics/sword/',
    'graphic': './graphics/sword/full.png'
}

SPELLS = {
    'fireball': {
        'power': 5,
        'worth': 20,
        'graphic': './graphics/spells/fireball/fireball.png',
        'sound': './audio/spells/fireball.wav'
    },
    'heal': {
        'power': 20,
        'worth': 10,
        'graphic': './graphics/spells/heal/heal.png',
        'sound': './audio/spells/heal.wav'
    }
}

PLAYER_STATUSES = {
    'U': 'up',
    'D': 'down',
    'L': 'left',
    'R': 'right',

    'UI': 'up_idle',
    'DI': 'down_idle',
    'LI': 'left_idle',
    'RI': 'right_idle',

    'UA': 'up_attack',
    'DA': 'down_attack',
    'LA': 'left_attack',
    'RA': 'right_attack'
}

MONSTER_STATUSES = {
    'I': 'idle',
    'M': 'move',
    'A': 'attack'
}

MONSTERS = {
    'path': './graphics/monsters/',
    'boss': 'frog',

    'cyclope': {
        'hp': 120,
        'damage': 25,
        'experience': 200,
        'speed': 3,
        'resistance': 2,
        'attack_radius': 50,
        'notice_radius': 250,
        'hitbox_offset': (-10, -30),
        'attack_cooldown': 500,
        'invulnerability_duration': 800,
        'attack_type': 'thunder',
        'attack_sound': './audio/fight/thunder.wav',
        'hit_sound': './audio/fight/hit_2.wav',
        'death_sound': './audio/fight/death_1.wav'
    },
    'leszy': {
        'hp': 100,
        'damage': 30,
        'experience': 190,
        'speed': 3,
        'resistance': 2,
        'attack_radius': 40,
        'notice_radius': 300,
        'hitbox_offset': (-10, -30),
        'attack_cooldown': 500,
        'invulnerability_duration': 800,
        'attack_type': 'leafs',
        'attack_sound': './audio/fight/leafs.wav',
        'hit_sound': './audio/fight/hit_1.wav',
        'death_sound': './audio/fight/death_1.wav'
    },
    'raccoon': {
        'hp': 80,
        'damage': 20,
        'experience': 160,
        'speed': 4,
        'resistance': 3,
        'attack_radius': 60,
        'notice_radius': 320,
        'hitbox_offset': (-10, -30),
        'attack_cooldown': 400,
        'invulnerability_duration': 700,
        'attack_type': 'slash',
        'attack_sound': './audio/fight/slash.wav',
        'hit_sound': './audio/fight/hit_3.wav',
        'death_sound': './audio/fight/death_1.wav'
    },

    'frog': {
        'hp': 500,
        'damage': 90,
        'experience': 1000,
        'speed': 2,
        'resistance': 2,
        'attack_radius': 100,
        'notice_radius': 500,
        'hitbox_offset': (-10, -50),
        'attack_cooldown': 1000,
        'invulnerability_duration': 1000,
        'attack_type': 'claws',
        'attack_sound': './audio/fight/claws.wav',
        'hit_sound': './audio/fight/hit_2.wav',
        'death_sound': './audio/fight/death_2.wav'
    }
}
