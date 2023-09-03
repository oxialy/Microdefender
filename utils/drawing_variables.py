import pygame.font
import math

from math import pi, cos, sin

pygame.font.init()


hexagon = [
    (cos(0), sin(0)),
    (cos(pi * 1/3), sin(pi * 1/3)),
    (cos(pi * 2/3), sin(pi * 2/3)),
    (cos(pi * 3/3), sin(pi * 3/3)),
    (cos(pi * 4/3), sin(pi * 4/3)),
    (cos(pi * 5/3), sin(pi * 5/3))
]




colors = {
    'blue1': '#102050',
    'blue2': '#103499',
    'blue3': '#003899',
    'darkblue': '#121240',
    'lightblue': '#303098',
    'red1': '#400020',
    'red2': '#800000',
    'seagreen': '#004040',
    'light_green': '#009060',
    'yellow': '#A29870',
    'orange': '#bb7000',
    'darkgreen': '#105020',
    'white': '#AAAAAA',
    'grey': '#607080',
    'lightgrey': '#809098',
    'darkgrey': '#304040',
    'darkblue1': '#102030',
    'cyan': '#105080',
    'black': '#000000'
}

bg_color = '#0D1913'






FONT15 = pygame.font.SysFont('arial', 15)
FONT20 = pygame.font.SysFont('arial', 20)
FONT25 = pygame.font.SysFont('arial', 25)


def scale_polygon(poly, scaling):
    scaled_poly = []

    for p in poly:
        x,y = p

        scaled_x = x * scaling
        scaled_y = y * scaling

        scaled_poly.append((scaled_x, scaled_y))

    return scaled_poly

def shift_polygon(poly, dist):
    shifted_poly = []

    for p in poly:
        x,y = p

        shifted_x = x + dist
        shifted_y = y + dist

        shifted_poly.append((shifted_x, shifted_y))

    return shifted_poly




