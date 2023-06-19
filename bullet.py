import pygame

from settings import *
from groups import *



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, shooter, bullet_image, bullet_damage=5):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 23
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.shooter = shooter
        self.bullet_damage = bullet_damage
        
        
    def update(self):
        from static_objects import world, player
        from game_world import Enemy, EnemyBoss, EnemySergant
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
                player.is_hit = True
                player.health -= self.bullet_damage
                self.kill()
        for enemy in enemy_group:        
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if isinstance(self.shooter, Enemy) or isinstance(self.shooter, EnemySergant)\
                    or isinstance(self.shooter, EnemyBoss):
                    # print("bot nie dostal, a mogl dostac")
                    pass
                elif enemy.alive:
                    enemy.is_hit = True
                    enemy.health -= 50
                    self.kill()
                    
