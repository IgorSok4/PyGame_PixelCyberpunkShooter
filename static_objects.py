from settings import *
from game_world import World, img_list
from groups import *

world = World(img_list, 'level3_przeszkody.csv')

player = world.player
healthbar = world.healthbar

def reset_static_objects():
    global world, player, healthbar
    world.reset_tiles()
    world_data = world.load_map('level3_przeszkody.csv')
    player, healthbar = world.process_tiles(world_data)
    
    return world, player, healthbar