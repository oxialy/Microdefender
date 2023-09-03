from utils.settings import UNIT_SPEC, WIDTH, HEIGHT
from utils.game_functions import Bunker, Banshee

import math
import random

from pygame import Vector2
from math import pi, sin, cos


DIRECTIONS = {
    'up'   : Vector2(0, -1),
    'down' : Vector2(0, 1),
    'left' : Vector2(-1, 0),
    'right': Vector2(1, 0)
}


def despawn_units():
    for unit in all_units:
        if unit.current_hp <= 0:
            all_units.remove(unit)
            unit.state = 'destroyed'


def create_player_team(units):
    player_units = []
    for unit in units:
        if unit.TEAM == 'player':
            player_units.append(unit)
    return player_units

def create_enemy_team(units):
    enemy_units = []
    for unit in units:
        if unit.TEAM == 'enemy':
            enemy_units.append(unit)
    return enemy_units

def create_all_banshee():
    for i in range(5):
        #RX, RY = random.randrange(20,WIDTH-30), random.randrange(0, 380)

        new_banshee = Banshee((200+i*50, 160-i*5), 11, 60, 3, 4, 0.2)
        all_units.append(new_banshee)




bunker1 = Bunker((250,500), 62, 200, 0, 7, 1)
#bunker2 = Bunker((320,500), 16, 120, 0, 7, 12)
bunker3 = Bunker((450,500), 40, 200, 0, 7, 1)

banshee1 = Banshee((500,100), 16, 200, 5, 4, 0.2, True)
banshee2 = Banshee((220,180), 15, 200, 5, 4, 0.2)

#bunker.update_hitbox()
banshee2.update_hitbox()
banshee1.update_hitbox()


all_units = [bunker1, bunker3, banshee2, banshee1]

#create_all_banshee()

player_units = create_player_team(all_units)
enemy_units = create_enemy_team(all_units)


idle_units = all_units.copy()
moving_units = []

selection = None



TOGGLE_MUTE = False
TOGGLE_INFO = True










