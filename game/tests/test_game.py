from utils.settings import *
from utils.support import *
from level.level import Level
from creatures.player import Player
from creatures.monster import Monster
from main import Game
import pygame
import pyautogui
import time


def test_import_layout():
    expected_layout_type = type([])
    expected_layout_unit = type('')

    path = MAP['layouts']['boundaries']
    map_layout = import_layout(path)

    assert type(map_layout) == expected_layout_type, 'Layout must be a 2D list'
    assert type(map_layout[0][0]) == expected_layout_unit, 'Unit must be a string'


def test_import_assets():
    pygame.display.init()
    pygame.display.set_mode((GAME_SETUP['width'], GAME_SETUP['height']))
    display_surf = pygame.display.get_surface()
    expected = type(display_surf)

    path = MAP['graphics']['small_objects']
    object_graphics = import_assets(path)

    assert type(object_graphics[0]) == expected, 'Imported asset must be a pygame.Surface'


def test_map_render():
    pygame.display.init()
    pygame.mixer.init()
    pygame.font.init()
    pygame.display.set_mode((GAME_SETUP['width'], GAME_SETUP['height']))
    level = Level()

    assert len(level.attacked_sprites) > 0, 'There must be attacked sprites (monsters) after rendering map'
    assert len(level.barrier_sprites) > 0, 'There must be barrier sprites (boundaries) after rendering map'
    assert len(level.visible_sprites) > 0, 'There must be visible sprites (objects, sprites) after rendering map'


def test_player_get_damage():
    pygame.display.init()
    pygame.mixer.init()
    pygame.font.init()
    pygame.display.set_mode((GAME_SETUP['width'], GAME_SETUP['height']))
    level = Level()
    start_hp = level.player.hp
    level.player_get_damage(MONSTERS['cyclope']['damage'], MONSTERS['cyclope']['attack_type'])
    damaged_hp = level.player.hp

    assert start_hp > damaged_hp, 'After getting damage hp of the player must decrease'


def test_player_get_experience():
    pygame.display.init()
    pygame.mixer.init()
    pygame.font.init()
    pygame.display.set_mode((GAME_SETUP['width'], GAME_SETUP['height']))
    level = Level()
    start_exp = level.player.experience
    level.player_get_experience(MONSTERS['cyclope']['experience'])
    increased_exp = level.player.hp

    assert start_exp < increased_exp, 'After getting experience the value of player attribute must increase'


def test_player_attacks():
    player = Player((0, 0), [], [], None, None, None)

    assert player.attack_sword() > 0, 'The damage value by the player\'s attack must be greater than 0'
    assert player.cast_spell() > 0, 'The damage value by the player\'s spell must be greater than 0'


def test_player_energy_regeneration():
    player = Player((0, 0), [], [], None, None, None)
    start_energy = player.energy
    player.energy_regeneration()
    increased_energy = player.energy

    assert start_energy < increased_energy, 'After regeneration energy value must increase'


def test_monster_status():
    player = Player((0, 0), [], [], None, None, None)
    monster = Monster(MAP['layouts']['monster_tiles']['0'], (1, 1), [], [], None, None, None)
    start_status = monster.status
    monster.process_status(player)
    changed_status = monster.status

    assert start_status != changed_status, 'If player is inside the notice and attack area -> status changes'


def test_monster_get_damage():
    player = Player((0, 0), [], [], None, None, None)
    monster = Monster(MAP['layouts']['monster_tiles']['0'], (1, 1), [], [], None, None, None)
    start_hp = monster.hp
    monster.get_damage(player, 'spell')
    damaged_hp_spell = monster.hp
    monster.get_damage(player, 'sword')
    damaged_hp_sword = monster.hp

    assert start_hp > damaged_hp_spell, 'After spell attack monster hp must decrease'
    assert start_hp > damaged_hp_sword, 'After sword attack monster hp must decrease'


def test_start_menu_play_btn():
    expected = True

    screen = pyautogui.size()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if game.start_menu.is_game_started:
            pygame.quit()
            break

        game.start_menu.render()
        pygame.display.update()
        game.clock.tick(GAME_SETUP['fps'])

        if pyautogui.position() != screen:
            time.sleep(2)
            pyautogui.moveTo(screen[0] // 2, screen[1] // 2)
            pyautogui.doubleClick()
        pyautogui.keyDown('space')

    assert game.start_menu.is_game_started == expected, 'If PLAY button is pressed than game starts'
