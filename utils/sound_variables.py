import pygame.mixer

pygame.mixer.init()


channel0 = pygame.mixer.Channel(0)
channel1 = pygame.mixer.Channel(1)
channel2 = pygame.mixer.Channel(2)
channel3 = pygame.mixer.Channel(3)
channel4 = pygame.mixer.Channel(4)
channel5 = pygame.mixer.Channel(5)
channel6 = pygame.mixer.Channel(6)
channel7 = pygame.mixer.Channel(7)

all_channels = [channel0, channel1, channel2, channel3, channel4, channel5, channel6, channel7]



global_path = './sound_effects/'


files1 = ['pack1-d.wav', 'pack1-e.wav', 'pack1-f.wav', 'pack1-g.wav']
files2 = ['pack2-a.wav','pack2-b.wav','pack2-c.wav','pack2-e.wav','pack2-f.wav','pack2-f4.wav']
files3 = ['pack3-a.wav','pack3-b.wav','pack3-d','pack3-e.wav','pack3-g.wav']
files4 = ['pack4-a.wav','pack4-a3.wav','pack4-b.wav','pack4-d.wav','pack4-d3.wav','pack4-f.wav','pack4-f3.wav']


def create_sound_dict(files):
    sound_dict = {}

    for file in files:
        sound_dict[file] = pygame.mixer.Sound(global_path + file)

    return sound_dict



