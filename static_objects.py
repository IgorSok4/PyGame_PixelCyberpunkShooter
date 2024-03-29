from settings import *
from game_world import World, img_list
from groups import *
from globals import g

world = World(img_list, f'level{g.level}_przeszkody.csv')


player = world.player
healthbar = world.healthbar

collected_money = player.money

def reset_static_objects():
    global world, player, healthbar
    world.reset_tiles()
    world_data = world.load_map(f'level{g.level}_przeszkody.csv')
    player, healthbar = world.process_tiles(world_data)
    
    return world, player, healthbar