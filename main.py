import random

from utils import settings
from utils import game_variables as GV
from utils import game_functions as GF
from utils.settings import clock, WIN, FPS

from utils.drawing_functions import draw_screen

from utils import sound_functions


import pygame
import math
import random

from pygame import Vector2
from math import pi, sin, cos


pygame.init()



main_run = True

selection = None

while main_run:

    draw_screen(WIN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                main_run = False



            if event.key == pygame.K_m:
                GV.TOGGLE_MUTE = not GV.TOGGLE_MUTE
                sound_functions.toggle_mute()

            if event.key == pygame.K_SPACE:
                for unit in GV.all_units:
                    if unit.TEAM == 'enemy':
                        unit.check_for_enemy_no_range(GV.all_units)

            if event.key == pygame.K_s:
                GV.create_all_banshee()
                GV.enemy_units = GV.create_enemy_team(GV.all_units)
            if event.key == pygame.K_i:
                print(selection.pushing, selection.collision_list)


            if event.key == pygame.K_UP:
                GV.bunker1.lock_target(GV.banshee1)
                print(GV.all_units)

            elif event.key == pygame.K_DOWN:
                GV.bunker1.selected = not GV.bunker1.selected
                GV.banshee1.selected = not GV.banshee1.selected
                GV.banshee2.selected = not GV.banshee2.selected

            elif event.key == pygame.K_LEFT:
                GV.banshee1.set_destination((0, GV.banshee1.pos[1]))
                GV.banshee2.set_destination((0, GV.banshee2.pos[1]))

                GV.moving_units += [GV.banshee1, GV.banshee2]


        if pygame.mouse.get_pressed()[0]:
            settings.pos = pygame.mouse.get_pos()
            pos_x, pos_y = settings.pos

            if selection:
                selection.selected = False
                selection = None

            for unit in GV.all_units:

                if unit.rect.collidepoint(settings.pos):
                    unit.selected = True
                    selection = unit

                    break


        if pygame.mouse.get_pressed()[2]:
            settings.pos = pygame.mouse.get_pos()
            pos_x, pos_y = settings.pos

            if selection:
                pressed = GF.pressed_unit(settings.pos, GV.all_units)

                if pressed:
                    selection.set_destination(settings.pos, pressed)
                else:
                    selection.set_destination(settings.pos)

            print(GV.banshee1.collision_list,
                  GV.banshee1.pushing,
                  GV.banshee1.speed)


        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[2]:
                settings.pos = pygame.mouse.get_pos()


    GF.all_units_action(GV.all_units)

    if False:
        for unit in GV.enemy_units:
            if unit.state == 'idle':
                unit.check_for_enemy_no_range(GV.all_units)

    GV.despawn_units()


    if GV.banshee1.state == 'tp':
        GV.banshee1.teleport((500, GV.banshee1.pos[1]))
        GV.banshee1.set_destination((0, GV.banshee1.pos[1]))

    if GV.banshee2.state == 'tp':
        GV.banshee2.teleport((500,GV.banshee2.pos[1]))
        GV.banshee2.set_destination((0, GV.banshee2.pos[1]))


    clock.tick(FPS)
    pygame.display.update()