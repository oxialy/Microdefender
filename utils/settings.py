
from utils.drawing_variables import colors



import pygame
import math

from math import pi, sin, cos, atan2

from pygame import Vector2


WIDTH, HEIGHT = 700,650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


pos = pos_x, pos_y = 0,0


clock = pygame.time.Clock()

FPS = 15
BASE_VOLUME = 1



UNIT_SPEC = {
    'bunker': {'attack_cd': 15},
    'banshee': {'attack_cd': 15}
}








