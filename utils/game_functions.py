from utils import settings
from utils import drawing_variables as DV

from utils.settings import WIDTH, HEIGHT, UNIT_SPEC
from utils.drawing_variables import colors, scale_polygon
from utils.sound_functions import idle_channel

import pygame
import random
import math

from pygame import Vector2
from random import randrange
from math import pi, sin, cos, atan2, sqrt


class Unit:
    def __init__(self, pos, size, max_hp, speed, range, attack, check=False):
        self.check = check
        self.pos = Vector2(pos)
        self.x, self.y = self.pos
        self.size = size

        self.max_hp = max_hp
        self.current_hp = max_hp

        self.BASE_SPEED = speed
        self.speed = speed

        self.range = range * 20
        self.attack = attack
        self.MAX_ATTACK_CD = UNIT_SPEC['bunker']['attack_cd']
        self.attack_cd = 0

        self.direction = 0   # facing angle
        self.vec = Vector2(0,0)

        self.state = 'idle'
        self.target = None
        self.destination = None

        self.pushing = None
        self.pushing_unit = None
        self.collision_list = set()

        self.selected = False
        self.rect = pygame.Rect(
            (self.x - self.size/2, self.y - self.size/2),
            (self.size, self.size)
        )
        self.surf = pygame.Surface((self.size+2, self.size+2))

        self.animation_timer = 0
        self.firing_col = colors['yellow']


    def draw_hp_bar(self, win):
        x,y = self.pos

        bar_size = self.max_hp // 2
        current_bar_size = self.current_hp // 2
        bar_pos = x - bar_size//2, y - self.size/2 - 18

        pygame.draw.rect(
            win, colors['grey'], (bar_pos, (bar_size, 3))
        )
        pygame.draw.rect(
            win, colors['blue3'], (bar_pos, (current_bar_size, 3))
        )

    def move(self):
        self.pos += self.vec * self.speed

        self.x, self.y = self.pos

        self.set_vector(self.destination)

        self.update_hitbox()


    def set_vector(self, destination):
        self.direction = angle = get_angle(self.pos, destination)

        self.vec = Vector2(cos(angle), sin(angle))


    def take_damage(self, dmg):
        self.current_hp -= dmg

    def fire(self, target):
        self.attack_cd = self.MAX_ATTACK_CD
        target.take_damage(self.attack)

        self.state = 'firing'

        if target.current_hp <= 0:
            self.unlock_target()



    def decrease_attack_cd(self):
        self.attack_cd -= 1
        self.attack_cd = max(0, self.attack_cd)

    def lock_target(self, target):
        self.target = target

    def unlock_target(self):
        self.target = None

    def in_range(self, target):

        dist = get_dist(self.pos, target.pos)

        return dist <= self.range

    def update_hitbox(self):
        x,y = self.pos
        w,h = self.size, self.size

        self.rect = pygame.Rect(
            (x-w/2, y-h/2), (w, h))

    def check_for_enemy(self, units):
        for unit in units:
            if self.in_range(unit) and unit.current_hp >= 0 and unit.TEAM != self.TEAM:
                self.lock_target(unit)

    def check_for_enemy_no_range(self, units):
        units_dist = {}

        for unit in units:
            if unit.current_hp >= 0 and unit.TEAM != self.TEAM:
                dist = get_dist(self.pos, unit.pos)
                units_dist[dist] = unit

        if units_dist:
            shortest_dist = min(units_dist)
            self.lock_target(units_dist[shortest_dist])
        else:
            self.unlock_target()


    def check_destination(self):
        x2, y2 = self.destination

        if abs(x2 - self.x) < 3 and abs(y2 - self.y) < 3:
            self.state = 'idle'

    def update_destination(self):
        if self.target.state == 'destroyed':
            self.unlock_target()
            self.state = 'idle'
        else:
            self.destination = self.target.pos



    def set_destination(self, destination, target=None, state='move'):
        self.destination = destination
        self.set_vector(destination)

        self.target = target
        self.state = state


    def play_idle_animation(self):
        pass

    def play_moving_animation(self):
        pass

    def play_destroying_animation(self):
        pass

    def play_firing_animation(self):
        self.animation_timer += 1

        if self.animation_timer >= 8:
            self.end_animation()

    def end_animation(self):
        self.state = 'idle'
        self.animation_timer = 0

    def draw_firing(self, win):
        A1 = get_point_on_line(self.pos, self.direction, 15)
        B1 = get_point_on_line(self.pos, self.direction, 18)

        A2 = get_point_on_line(self.pos, self.direction - pi / 21, 15)
        B2 = get_point_on_line(self.pos, self.direction - pi / 21, 16)

        A3 = get_point_on_line(self.pos, self.direction + pi / 20, 15)
        B3 = get_point_on_line(self.pos, self.direction + pi / 20, 16)


        pygame.draw.line(win, self.firing_col, A1, B1)

        if self.animation_timer in [0,1,2, 5,6,7,8]:

            pygame.draw.line(win, self.firing_col, A2, B2)

            pygame.draw.line(win, self.firing_col, A3, B3)

    def check_collision(self, units):
        self.collision_list = set()

        for unit in units:
            if unit != self:
                if unit.rect.colliderect(self.rect):
                    self.collision_list.add(unit)

                    if not self.pushing:
                        if len(unit.collision_list) > 0:
                            self.speed /= len(unit.collision_list)
                            self.pushing = 'pushed'

                        elif self.state == 'move':
                            self.pushing = 'pushing'
                            self.speed = 1

                        else:
                            self.pushing = 'pushed'

                        self.pushing_unit = unit


        if self.pushing_unit not in self.collision_list:
            self.speed = self.BASE_SPEED
            self.pushing = None


    def push(self):
        pushed = self.pushing_unit
        angle = get_angle(self.pos, pushed.pos)

        pos_90_rotation = get_rotated_angle(angle, pi/2)
        neg_90_rotation = get_rotated_angle(angle, -pi/2)

        pos_90_vector = Vector2(cos(pos_90_rotation), sin(pos_90_rotation))
        neg_90_vector = Vector2(cos(neg_90_rotation), sin(neg_90_rotation))

        if self.pushing == 'pushing':
            if self.direction - angle > 0:
                self.pos += pos_90_vector * self.speed
            else:
                self.pos += neg_90_vector * self.speed

        pushed.pos += Vector2(cos(angle), sin(angle)) * pushed.speed

        if self.check:
            print(self.pushing, self.collision_list, self.speed)

        self.update_hitbox()
        pushed.update_hitbox()



    
class Bunker(Unit):

    hexagon = [
        (cos(0) + 1, sin(0) + 1),
        (cos(pi * 1 / 3) + 1, sin(pi * 1 / 3) + 1),
        (cos(pi * 2 / 3) + 1, sin(pi * 2 / 3) + 1),
        (cos(pi * 3 / 3) + 1, sin(pi * 3 / 3) + 1),
        (cos(pi * 4 / 3) + 1, sin(pi * 4 / 3) + 1),
        (cos(pi * 5 / 3) + 1, sin(pi * 5 / 3) + 1),
    ]
    def __init__(self, pos, size, max_hp, speed, range, attack, check=False):
        super().__init__(pos, size, max_hp, speed, range, attack)

        self.shape = scale_polygon(self.hexagon, self.size/2)

        self.TEAM = 'player'
        self.firing_col = colors['yellow']


    def draw(self, win):
        draw_pos = draw_x, draw_y = self.x - self.size/2, self.y - self.size/2

        win.blit(self.surf, draw_pos)
        self.surf.fill(DV.bg_color)

        pygame.draw.polygon(self.surf, colors['red1'], self.shape)
        pygame.draw.polygon(self.surf, colors['grey'], self.shape, 4)

        start = self.x + cos(pi*4/3)*(self.size-7)/2, self.y + sin(pi*4/3)*(self.size-7)/2
        end = self.x + cos(pi*1/3)*(self.size-7)/2, self.y + sin(pi*1/3)*(self.size-7)/2
        #pygame.draw.line(win, colors['dark_blue'], start, end, 3)


        if self.state == 'firing':
            self.draw_firing(win)

        if self.selected:
            pygame.draw.circle(win, colors['blue1'], self.pos, self.range, 1)

        pygame.draw.circle(win, colors['grey'], self.pos, 3)



class Banshee(Unit):
    def __init__(self, pos, size, max_hp, speed, range, attack, check=False):
        super().__init__(pos, size, max_hp, speed, range, attack)

        self.TEAM = 'enemy'
        self.firing_col = colors['red2']
        self.check = check


    def draw(self, win):
        x,y,w,h = self.rect

        pygame.draw.ellipse(win, colors['black'], self.rect)
        pygame.draw.ellipse(win, colors['blue2'], self.rect, 3)
        #pygame.draw.ellipse(win, colors['red1'], (x+4,y+4, 4,4))


        if self.state == 'firing':
            self.draw_firing(win)

        if self.selected:
            pygame.draw.circle(win, colors['blue2'], self.pos, self.range, 1)



def get_dist(A, B):
    x1, y1 = A
    x2, y2 = B

    return sqrt((x2-x1)**2 + (y2-y1)**2)



def get_angle(A, B):
    x1, y1 = A
    x2, y2 = B

    angle = atan2((y2 - y1), (x2 - x1))

    return angle

def get_rotated_angle(angle, rotation):
    return angle + rotation



def get_point_on_line(pos, angle, dist):
    x0, y0 = pos

    x = cos(angle) * dist + x0
    y = sin(angle) * dist + y0

    return x, y


def all_units_action(units):
    for unit in units:
        if unit.target and unit.in_range(unit.target):
            unit.set_vector(unit.target.pos)

        if unit.target and unit.attack_cd == 0:
            if unit.in_range(unit.target):
                unit.fire(unit.target)
            else:
                unit.set_destination(unit.target.pos, unit.target)
        
        if unit.state in ['move', 'attack_move']:
            unit.move()
            unit.check_destination()

            if unit.target:
                if unit.in_range(unit.target):
                    unit.fire(unit.target)
                else:
                    unit.update_destination()

        if unit.state in ['idle', 'attack_move'] and not unit.target:
            unit.check_for_enemy(units)

        if unit.attack_cd >= 0:
            unit.decrease_attack_cd()

        unit.check_collision(units)

        if unit.pushing:
            unit.push()

        play_animation(unit)


def fire_all(units):
    for unit in units:
        if unit.target in units and unit.attack_cd <= 0 and unit.in_range(unit.target):
            unit.fire(unit.target)


def move_all(units):
    for unit in units:
        unit.move()

def decrease_cd_all(units):
    for unit in units:
        unit.decrease_attack_cd()

def check_for_enemy_all(units, enemies):
    for unit in units:
        unit.check_for_enemy(enemies)

def check_destination_all(units):
    for unit in units:
        unit.check_destination()


def animate_all(units):
    for unit in units:
        play_animation(unit)

def play_animation(unit):
    anim = {
        'idle': unit.play_idle_animation,
        'firing': unit.play_firing_animation,
        'move': unit.play_moving_animation,
        'destroying': unit.play_destroying_animation
    }

    anim[unit.state]()

def pressed_unit(pos, units):
    for unit in units:
        if unit.rect.collidepoint(pos):
            return unit






