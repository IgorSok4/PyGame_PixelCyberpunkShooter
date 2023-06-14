import pygame

from explosions import Explosion
from static_objects import *
from groups import *
from globals import g


#load images

grenade_img = pygame.image.load('media/other/grenade/idle/0.png')
grenade_img = pygame.transform.scale(grenade_img, (grenade_img.get_width() * 1.5, grenade_img.get_height() * 1.5))


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.bounce_count = 0
        self.bounce_height = 10  # Wysokość pierwszego odbicia granatu
        self.bounce_ratio = 0.5  # Współczynnik zmniejszania wysokości odbicia
        
    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y
        
        # Check collision with the tiles
        for tile in world.obstacle_list:
            # Check x collision
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
                self.direction *= -1
            # Check y collision
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.vel_y < 0:  # hitting the top of the tile
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:  # hitting the bottom of the tile
                    dy = tile[1].top - self.rect.bottom
                    self.bounce_count += 1
                    if self.bounce_count < 3:
                        self.vel_y = -self.bounce_height  # Change the direction of grenade's vertical speed
                        self.bounce_height *= self.bounce_ratio  # Decrease the bounce height
                    else:
                        self.speed = 0  # If the grenade hits the floor, it stops

        #grenade out of screen
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            self.direction *= -1
        
        #update grenade position
        self.rect.x += dx + g.screen_scroll
        self.rect.y += dy

        #countdown times
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 1, self.rect)
            explosion_group.add(explosion)
            #damage
            distance_to_player = max(abs(self.rect.centerx - player.rect.centerx), abs(self.rect.centery - player.rect.centery))
            if distance_to_player < TILE_SIZE * 3:
                damage_ratio = (TILE_SIZE * 3 - distance_to_player) / (TILE_SIZE * 3)  # to create a ratio between 0 and 1
                player.health -= 10 * damage_ratio  # scale the damage accordingly

            for enemy in enemy_group:
                distance_to_enemy = max(abs(self.rect.centerx - enemy.rect.centerx), abs(self.rect.centery - enemy.rect.centery))
                if distance_to_enemy < TILE_SIZE * 3:
                    damage_ratio = (TILE_SIZE * 3 - distance_to_enemy) / (TILE_SIZE * 3)  # to create a ratio between 0 and 1
                    enemy.health -= 10 * damage_ratio  # scale the damage accordingly