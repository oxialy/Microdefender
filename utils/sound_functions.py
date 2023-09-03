from utils import settings
from utils import game_variables as GV

from utils.sound_variables import all_channels


import pygame.mixer


def toggle_mute():
    if GV.TOGGLE_MUTE:
        set_volume(0)
    else:
        set_volume(settings.BASE_VOLUME)


def set_volume(vol):

    for channel in all_channels:
        channel.set_volume(vol)



def idle_channel(channels):
    for channel in channels:
        if not channel.get_busy():
            return channel

    return channels[0]

def play_sound(sound):
    idle_channel(all_channels).play(sound)








