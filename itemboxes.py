import pygame

from settings import *
from globals import g



class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_taken = False
        self.images = []
        self.item_type = item_type
        for i in range(0, 5):
            img = pygame.image.load(f'media/other/{self.item_type}/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * 0.5), int(img.get_height() * 0.5)))
            self.images.append(img)

        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.counter = 0
        self.is_animating = False
        
    def update(self):
        from static_objects import player
        #map scroll update
        self.rect.x += g.screen_scroll

        OPEN_BOX_SPEED = 5
        #rotating money
        self.counter += 1
        if pygame.sprite.collide_rect(self, player):
            self.is_animating = True
        if self.item_type == 'money':
            if self.counter >= OPEN_BOX_SPEED:
                self.counter = 0 
                self.frame_index += 1 
                if self.frame_index >= len(self.images):
                    if self.is_animating:  # money disappears when the player is near
                        self.kill()
                        player.money += 5
                    else:  # restart the animation
                        self.frame_index = 0
                # update image only when frame_index is within range
                if self.frame_index < len(self.images):
                    self.image = self.images[self.frame_index]
                    
        #other itemboxes - no animation during the loop. Animation only when player collide with object
        if self.is_animating:
            if self.counter >= OPEN_BOX_SPEED:
                self.counter = 0
                # continue the animation even when player is not colliding
                if self.item_type == "grenade_box":
                    if self.frame_index == 0:
                        item_pickup_sound.play()
                    if not self.item_taken:
                        self.frame_index += 1    
                        player.grenades += 2
                        if self.frame_index >= len(self.images):
                            pass
                        else:
                            self.image = self.images[self.frame_index]
                        if player.grenades > 3:
                            player.grenades = player.max_grenades
                    if self.frame_index == 5:
                        self.item_taken = True
                elif self.item_type == "ammo_box":
                    if self.frame_index == 2:
                        biker_reload_sound.play()
                    if not self.item_taken:
                        self.frame_index += 1 
                        player.ammo += 20
                        if self.frame_index >= len(self.images):
                            pass
                        else:
                            self.image = self.images[self.frame_index]
                        if player.ammo > 40:
                            player.ammo = 40
                    if self.frame_index == 5:
                        self.item_taken = True