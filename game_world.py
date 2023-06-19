import pygame
import random
import csv

from characters import MainCharacter, Enemy, EnemySergant
from settings import TILE_TYPES, screen, exit_sign
from groups import *
from healthbar import HealthBar
from itemboxes import *
from globals import g


# load images
# tiles
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'media/map/level1/tiles/{x}.png') 
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

class World:
    def __init__(self, tile_images, map_file):
        self.tiles = tile_images
        self.map_data = self.load_map(map_file)
        self.obstacle_list = []
        self.decoration_list = []
        self.player = None
        self.healthbar = None
        self.map_img = None 
        self.process_tiles(self.map_data)

    
    def load_map(self, map_file):
        with open(map_file, 'r') as file:
            return list(csv.reader(file, delimiter=';'))

    def process_tiles(self, data):
        
        self.map_img = pygame.Surface((len(self.map_data[0]) * TILE_SIZE, len(self.map_data) * TILE_SIZE))

        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                tile = int(tile)
                if tile >= 0:
                    img = self.tiles[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 16 or 44 <= tile <= 45: 
                        self.obstacle_list.append(tile_data)
                    elif 17 <= tile <= 36:
                        self.decoration_list.append(tile_data)
                    elif tile == 37:
                        player = MainCharacter(x * TILE_SIZE, y * TILE_SIZE, 1.5, 5, 20) #(x, y, scale, speed. ammo)
                        healthbar = HealthBar(10, 10, player.health, player.max_health)
                        self.player = player
                        self.healthbar = healthbar
                    elif tile == 38:
                        ai_state = random.choice(["on", "off", "off"])
                        enemy = Enemy(x * TILE_SIZE, y * TILE_SIZE, 1.5, 3, ai_status=ai_state)
                        enemy_group.add(enemy)
                    elif tile == 39: #create money
                        item_box = ItemBox("money", x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 40: #create ammo_box
                        item_box = ItemBox("ammo_box", x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 41: #create grenade_box
                        item_box = ItemBox("grenade_box", x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 42: #create sergant
                        enemy = EnemySergant(x * TILE_SIZE, y * TILE_SIZE, 1.5, 3)
                        enemy_group.add(enemy)
                    elif tile == 43: #exit level
                        exit_sign = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        self.decoration_list.append(exit_sign)

        

        return player, healthbar

    def draw(self):
        for tile in self.decoration_list:
            if isinstance(tile, tuple):
                tile[1][0] += g.screen_scroll
                screen.blit(tile[0], tile[1])
            else:
                tile.x += g.screen_scroll
                screen.blit(exit_sign, (tile.x, tile.y))

        
        for tile in self.obstacle_list:
            tile[1][0] += g.screen_scroll
            screen.blit(tile[0], tile[1])
            
    
    def reset_tiles(self):
        self.obstacle_list = []
        self.decoration_list = []
