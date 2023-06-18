import pygame

from settings import *
from groups import *


#load images
bullet_img = pygame.image.load('media/bullet/ak.png')

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, shooter):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 23
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.shooter = shooter
        
        
    def update(self):
        from static_objects import world, player
        from game_world import Enemy
        #move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #bullet out of screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()


        #collision with map
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        
            
        # check collision with characters
        
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                # print("Player dostal")
                player.update_action(5)
                player.health -= 5
                self.kill()
        for enemy in enemy_group:        
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if isinstance(self.shooter, Enemy):
                    # print("bot nie dostal, a mogl dostac")
                    pass
                elif enemy.alive:
                    enemy.health -= 50
                    self.kill()
                    
