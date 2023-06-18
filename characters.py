import pygame
import glob
import random

from settings import *
from groups import *
from bullet import Bullet
from globals import g



class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, ammo=0):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = "player"
        self.pers_type = "biker"
        # self.pose_type = pose_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.grenades = 3
        self.max_grenades = self.grenades
        self.health = 100
        self.max_health = self.health
        self.money = 0
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.scale = scale
        self.scroll_start = 600
       

        
        # load all images
        animation_types = ['idle2', 'walk2', 'jump', 'death', 'shoot2', 'hit']
        
        for animation in animation_types:
            # temp_list resets temporaty list of images
            temp_list = []
            
            # count amount of files (images) in folder - to use in for loop
            folder_path = f'media/{self.char_type}/{self.pers_type}/{animation}'
            file_count = len(glob.glob(folder_path + '/*'))
            # print(f'{animation} : {file_count}')
            for i in range(file_count):
                img = pygame.image.load(f'media/{self.char_type}/{self.pers_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
    
        
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        
    def update(self):
        self.update_animation()
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


    def move(self, moving_left, moving_right):
        from static_objects import world
        #reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0

        #assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
            
        #jump
        if self.jump == True and self.in_air == False:
            #jump height
            self.vel_y = -15 # y coordinate starts at 0 at the top of the screen and increases as you go down
            self.jump = False
            self.in_air = True

        # gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # player psyhics with loaded tiles - mess
        self.in_air = True

        for tile in world.obstacle_list:
            # horizontal collisions
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
            # Check for vertical collisions
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                # if jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # if falling
                elif self.vel_y >= 0:
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
                    
                    
        #if fallen out of the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        #scroll
        if self.char_type == 'player':
            if (self.rect.right > self.scroll_start and moving_right) and self.rect.right < COLS*32:
                self.rect.x -= dx
                screen_scroll = -dx
            elif (self.rect.left < SCROLL_THRESH and moving_left):
                if self.rect.left > 0:
                    self.rect.x -= dx
                    screen_scroll = -dx
                else:
                    screen_scroll = 0


        return screen_scroll



        
    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + int(0.75 * self.rect.size[0] * self.direction),\
                            self.rect.centery - int(0.22 * self.rect.size[0]), self.direction, self)
            bullet_group.add(bullet)
            self.ammo -= 1
        
        
    def update_animation(self):
        ANIMATION_COOLDOWN = 50
        #update image depeding on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enought time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # index error fix
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
             
    
    def update_action(self, new_action):
        #if new_action is different from current one
        if new_action != self.action:
            self.action = new_action
            #update animation
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            
        
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
        

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Enemy(MainCharacter):
    def __init__(self, x, y, scale, speed, char_type="enemy", pers_type="officer", ai_status="on"):
        super().__init__(x, y, scale, speed)
        self.char_type = char_type
        self.pers_type = pers_type
        self.health = 100
        self.ammo = 1000
        self.shoot_cooldown = 0
        self.animation_list = []
        #ai
        self.ai_status = ai_status
        self.move_counter = 0
        self.idling = True
        self.idling_counter = 0
        self.vision = pygame.Rect(0, 0, 400, 20) #400 - enemies' sight
        

        
        animation_types = ['idle', 'walk', 'death', 'shoot', 'hit']
        
        for animation in animation_types:
            # temp_list resets temporaty list of images
            temp_list = []
            
            # count amount of files (images) in folder - to use in for loop
            folder_path = f'media/{self.char_type}/{self.pers_type}/{animation}'
            file_count = len(glob.glob(folder_path + '/*'))
            # print(f'{animation} : {file_count}')
            for i in range(file_count):
                img = pygame.image.load(f'media/{self.char_type}/{self.pers_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
    
        
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        
        
    def ai(self):
        from static_objects import player
        if self.alive and player.alive:   
            if self.idling == False and random.randint(1, 100) == 10:
                self.update_action(0) #idling
                self.idling = True
                # if self.ai_status == "off":
                #     self.idling_counter = random.randint(500, 2000)
                # else:
                self.idling_counter = random.randint(20, 100)
            #if ai in near the player
            if self.vision.colliderect(player.rect):
                if self.health < 30:
                    self.speed += self.speed * 0.5
                    self.direction *= -1
                    if self.direction == 1:
                        ai_move_right = True
                    else:
                        ai_move_right = False
                else:
                    self.update_action(3) #idling
                    self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_move_right = True
                    else:
                        ai_move_right = False
                    ai_move_left = not ai_move_right
                    self.move(ai_move_left, ai_move_right)
                    self.update_action(1) #run
                    self.move_counter += 1
                    #update vision with move
                    self.vision.center = (self.rect.centerx + 75 * self.direction,\
                                        self.rect.centery)
                    # pygame.draw.rect(screen, RED, self.vision)
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
                        
        #scroll
        self.rect.x += g.screen_scroll
        
        
    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        #update image depeding on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enought time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # index error fix
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 2:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
        
        
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(2)
            