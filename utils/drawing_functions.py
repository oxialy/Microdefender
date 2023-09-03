from utils import settings
from utils import game_variables as GV

from utils.settings import WIDTH, HEIGHT

from utils.drawing_variables import colors, bg_color, FONT15, FONT20, FONT25
from utils.game_variables import all_units

import pygame


def draw_screen(win):
    win.fill(bg_color)

    draw_unit(win, all_units)



    if GV.bunker1.target:
        write_text(win, GV.bunker1.target.pos, (WIDTH-70, 25))
        write_text(win, GV.bunker1.target.current_hp, (WIDTH-70, 50))

    if GV.selection:
        unit = GV.selection
        write_text(win, unit.pos, (WIDTH-70, 80))
        write_text(win, unit.target, (WIDTH-70, 105))

    # Y axis
    #pygame.draw.line(win,'#404040', (WIDTH/2, 0), (WIDTH/2, HEIGHT))


def draw_unit(win, units):
    for unit in units:
        unit.draw(win)
        unit.draw_hp_bar(win)


def draw_crosshair(win):   # screen middle crossbar

    pygame.draw.rect(win, 'purple', (WIDTH/2-4, HEIGHT/2, 8,1))
    pygame.draw.rect(win, 'purple', (WIDTH / 2, HEIGHT / 2 - 4, 1, 8))

def display_control(win):

    controls = {

        'spawn ball': '1 - 2 - 3',
        'autospawn ball': 'A',
        'spawn 3 random walls': 'W',
        'undo wall': 'U',
    }

    for i, (control, key) in enumerate(controls.items()):
        text_pos1 = 30, 50 + i*28
        text_pos2 = 120, 50 + i*28

        write_text(win, control, text_pos1)
        write_text(win, key, text_pos2)




def write_text(win, data, pos, font=FONT15):
    x,y = pos

    text_surf = font.render(str(data), 1, '#A09040')
    win.blit(text_surf, (x,y))

