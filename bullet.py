import pygame

# #load images
# #bullet
# bullet_img = pygame.image.load('media/bullet/2.png')


# class Bullet(pygame.sprite.Sprite):
#     def __init__(self, x, y, direction, screen_width, player):
#         pygame.sprite.Sprite.__init__(self)
#         self.speed = 23
#         self.image = bullet_img
#         self.rect = self.image.get_rect()
#         self.rect.center = (x, y)
#         self.direction = direction
#         self.screen_width = screen_width
#         self.player = player
        
#     def update(self):
#         #move bullet
#         self.rect.x += (self.direction * self.speed)
#         #bullet out of screen
#         if self.rect.right < 0 or self.rect.left > self.screen_width:
#             self.kill
            
#         # check collision with characters
        
#         if pygame.sprite.spritecollide(self.player, bullet_group, False):
#             if self.player.alive:
#                 self.kill
                
#         if pygame.sprite.spritecollide(self.player, bullet_group, False):
#             if self.player.alive:
#                 self.kill
        
        
# #create sprite groups
# bullet_group = pygame.sprite.Group()
