import pygame
import glob
from bullet import *


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

#set framerate
clock = pygame.time.Clock()
FPS = 60

#game variables
GRAVITY = 0.75
TILE_SIZE = 40


# define player actions variables
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

#load images
#bullet
bullet_img = pygame.image.load('media/bullet/2.png')
#grenade
grenade_img = pygame.image.load('media/other/grenade/idle/0.png')
grenade_img = pygame.transform.scale(grenade_img, (grenade_img.get_width() * 1.5, grenade_img.get_height() * 1.5))
#pick up boxes items
# animation_list_boxes_items = []
# animation_types_boxes_items = ['money', 'grenade_box', 'ammo_box']

# for animation in animation_types_boxes_items:
#     # temp_list resets temporaty list of images
#     temp_list = []
    
#     folder_path = f'media/other/{animation}'
#     file_count = len(glob.glob(folder_path + '/*'))
    
#     for i in range(file_count):
#         img = pygame.image.load(f'media/other/{animation}/{i}.png')
#         img = pygame.transform.scale(img, (int(img.get_width() * 1), int(img.get_height() * 1)))
#         temp_list.append(img)
#     animation_list_boxes_items.append(temp_list)
    
#     #animation_list_boxes_items[0] - money
#     #animation_list_boxes_items[1] - grenade_box
#     #animation_list_boxes_items[2] - ammo_box


# money_img = pygame.image.load('media/other/money/0.png')
# grenade_box_img = pygame.image.load('media/other/grenade_box/0.png')
# ammo_box_img = pygame.image.load('media/other/ammo_box/0.png')
# item_boxes = {
#     'Money':money_img,
#     'Grenade':grenade_box_img,
#     'Ammo':ammo_box_img
# }


#define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


#define font
font = pygame.font.SysFont('Futura', 30)

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))






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
       

        
        # load all images
        animation_types = ['idle', 'walk', 'jump', 'death', 'shoot']
        
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
        
        
    def update(self):
        self.update_animation()
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


    def move(self, moving_left, moving_right):
        #reset movement variables 
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
            self.vel_y = -10 # y coordinate starts at 0 at the top of the screen and increases as you go down
            self.jump = False
            self.in_air = True
        
        #gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y
        
        #chceck collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False
        

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy
        
    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + int(0.55 * self.rect.size[0] * self.direction),\
                            self.rect.centery - int(0.22 * self.rect.size[0]), self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1
        
        
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
    def __init__(self, x, y, scale, speed, char_type="enemy", pers_type="officer"):
        super().__init__(x, y, scale, speed)
        self.char_type = char_type
        self.pers_type = pers_type
        self.health = 100
        self.ammo = 1000
        self.shoot_cooldown = 0
        self.animation_list = []

        
        animation_types = ['idle', 'walk', 'death', 'shoot']
        
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
    
    

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_taken = False
        self.images = []
        self.item_type = item_type
        # self.image = item_boxes[self.item_type] #choosing item from dict available items
        # self.rect = self.image.get_rect()
        # self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        for i in range(0, 5):
            img = pygame.image.load(f'media/other/{self.item_type}/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * 1), int(img.get_height() * 1)))
            self.images.append(img)

        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.counter = 0
        
    def update(self):
        OPEN_BOX_SPEED = 5
        #update animation
        self.counter += 1
        if pygame.sprite.collide_rect(self, player):
            if self.counter >= OPEN_BOX_SPEED:
                self.counter = 0
                # collision with MainCharacter
                if self.item_type == 'money':
                    self.frame_index += 1 
                    player.money += 3
                    if self.frame_index >= len(self.images):
                        self.kill()
                    else:
                        self.image = self.images[self.frame_index]
                elif self.item_type == "grenade_box":
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








class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 23
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        
    def update(self):
        #move bullet
        self.rect.x += (self.direction * self.speed)
        #bullet out of screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
            
        # check collision with characters
        
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        for enemy in enemy_group:        
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()
                
                
                
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
        
        #chceck collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            #
            # Odbicie granatu od podłoża
            if self.bounce_count < 3:
                self.vel_y = -self.bounce_height  # Zmień kierunek pigonowej prędkości granatu
                self.bounce_height *= self.bounce_ratio  # Zmniejsz wysokość odbicia
                self.bounce_count += 1  # Zwiększ licznik odbić
            else:
                self.speed = 0  # Jeżeli granat dotknął zmieni na stale, zatrzymuje sie
                
            
        
        #grenade out of screen
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            self.direction *= -1
        
        #update grenade position
        self.rect.x += dx
        self.rect.y += dy
        
        #countdown times
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 1)
            explosion_group.add(explosion)
            #damage
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and\
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                    player.health -= 50
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and\
                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                        enemy.health -= 50
                
        


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
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
        self.counter = 0
        
        
    def update(self):
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

        
        
#create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()


# creating item boxes
item_box = ItemBox("money", 100, 260)
item_box_group.add(item_box)
item_box = ItemBox("ammo_box", 400, 260)
item_box_group.add(item_box)
item_box = ItemBox("grenade_box", 500, 260)
item_box_group.add(item_box)

# enemy2 = MainCharacter('player', 'biker', 200, 250, 3, 5, 20, 5)
# enemy = MainCharacter('enemy', 'officer', 400, 200, 3, 5, 10, 0)
# player = EnemyOfficer('enemy', 'officer', 500, 300, 3, 5) #(char_type, pers_type, x, y, scale, speed):

player = MainCharacter(200, 250, 3, 5, 20) #(char_type, pers_type, x, y, scale, speed):
enemy2 = Enemy(500, 300, 3, 5)
enemy = Enemy(400, 200, 3, 5)


enemy_group.add(enemy)
enemy_group.add(enemy2)


run = True
while run:
    
    clock.tick(FPS)
    
    draw_bg()
    
    #show ammo
    draw_text('AMMO: ', font, WHITE, 10, 35)
    if player.ammo <= 20:      
        for x in range(player.ammo):
            screen.blit(bullet_img, (90 + (x * 10), 40))
    else:
        rest_ammo = player.ammo - 20
        for x in range(20):
            screen.blit(bullet_img, (90 + (x * 10), 40))
        for y in range(rest_ammo):
            screen.blit(bullet_img, (90 + (y * 10), 30))
                
    #show grenades
    draw_text(f'GRENADE: {player.grenades}', font, WHITE, 10, 60)
    for x in range(player.grenades):
        screen.blit(grenade_img, (135 + (x * 15), 60))
    #show money
    draw_text(f'MONEY: {player.money}', font, WHITE, 10, 85)
    
    
    
    
    player.update()
    player.draw()
    
    for enemy in enemy_group:
        enemy.update()
        enemy.draw()
    
    #update and draw groups
    bullet_group.update()
    grenade_group.update()
    item_box_group.update()
    explosion_group.update()
    
    bullet_group.draw(screen)
    grenade_group.draw(screen)
    item_box_group.draw(screen)
    explosion_group.draw(screen)
    
    
    #update player actions
    if player.alive:
        #shoot
        if shoot:
            player.shoot()
            player.update_action(4)
        #grenades
        elif grenade and grenade_thrown == False and player.grenades > 0:
            grenade = Grenade(player.rect.centerx + int(0.55 * player.rect.size[0] * player.direction),\
                            player.rect.centery - int(0.7 * player.rect.size[0]), player.direction)
            grenade_group.add(grenade)
            grenade_thrown = True
            player.grenades -= 1
        elif player.in_air:
            player.update_action(2) # jump
        elif moving_left or moving_right:
            player.update_action(1) # run
        else:
            player.update_action(0) # idle
    
    player.move(moving_left, moving_right)
    
    for event in pygame.event.get():
         #quit game
        if event.type == pygame.QUIT:
             run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_g:
                grenade = True
                grenade_thrown = False
            if event.key == pygame.K_ESCAPE:
                run = False

             
        #keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_g:
                grenade = False   
            


    pygame.display.update()

pygame.quit()
