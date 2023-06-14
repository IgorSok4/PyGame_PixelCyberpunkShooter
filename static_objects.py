from settings import *
from game_world import World, img_list



world = World(img_list, 'level3_przeszkody.csv')

player = world.player
healthbar = world.healthbar


