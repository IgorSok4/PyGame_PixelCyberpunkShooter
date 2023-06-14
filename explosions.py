import pygame

from settings import *
from groups import *
from static_objects import player

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, grenade_rect):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        #loading photos to create animation
        for i in range(0, 12):
            img = pygame.image.load(f'media/other/grenade/explosion/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * 2.5), int(img.get_height() * 2.5)))
            self.images.append(img)
        # print(len(self.images))
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.grenade_rect = grenade_rect
        self.counter = 0
        
        
    def update(self):
        self.rect.x += screen_scroll
        EXPLOSION_SPEED = 7  #speed of an animation
        #update animation
        self.counter += 1
        print(self.counter)
        
        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]
        
        if self.frame_index == 6:  # on frame 2 of explosion, grenade deals another damage to the enemies/player
            distance_to_player = max(abs(self.grenade_rect.centerx - player.rect.centerx),
                                     abs(self.grenade_rect.centery - player.rect.centery))
            if distance_to_player < TILE_SIZE * 4:
                damage_ratio = (TILE_SIZE * 4 - distance_to_player) / (TILE_SIZE * 4)
                player.health -= 50 * damage_ratio

            for enemy in enemy_group:
                distance_to_enemy = max(abs(self.grenade_rect.centerx - enemy.rect.centerx),
                                        abs(self.grenade_rect.centery - enemy.rect.centery))
                if distance_to_enemy < TILE_SIZE * 4:
                    damage_ratio = (TILE_SIZE * 4 - distance_to_enemy) / (TILE_SIZE * 4)
                    enemy.health -= 50 * damage_ratio