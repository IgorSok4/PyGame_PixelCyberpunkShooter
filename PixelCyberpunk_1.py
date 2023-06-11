import pygame
import glob
from bullet import *
import random
import csv


pygame.init()


SCREENSIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 672

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('PixelCyberpunk')

clock = pygame.time.Clock()
FPS = 60

#game variables
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 21
COLS = 96
TILE_SIZE = 32
TILE_TYPES = 42
level = 1
screen_scroll = 0
bg_scroll = 0



# define player actions variables
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

# load images
# tiles
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'media/map/level1/tiles/{x}.png') 
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)


bullet_img = pygame.image.load('media/bullet/2.png')
grenade_img = pygame.image.load('media/other/grenade/idle/0.png')
grenade_img = pygame.transform.scale(grenade_img, (grenade_img.get_width() * 1.5, grenade_img.get_height() * 1.5))
background = pygame.image.load('media/map/level1/level3.png')

#define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


def draw_bg():
    screen.fill(BLACK)
    width = background.get_width()
    for x in range(5):
        screen.blit(background, ((x * width) - bg_scroll * 1, 0))


#define font
# font = pygame.font.SysFont('Futura', 30)

# def draw_text(text, font, text_color, x, y):
#     img = font.render(text, True, text_color)
#     screen.blit(img, (x, y))


# def draw_bg():
#     screen.fill(BG)
#     pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))



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

        # # start by assuming the character is in the air. This will be updated in the following logic
        self.in_air = True

        for tile in world.obstacle_list:
            # Check for horizontal collisions
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
            # Check for vertical collisions
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                # If we are above the ground i.e., jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # If we are below the ground i.e., falling
                elif self.vel_y >= 0:
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        #scroll
        if self.char_type == 'player':
            if self.rect.right > SCREEN_WIDTH - SCROLL_THRESH\
                or self.rect.left < SCROLL_THRESH:
                self.rect.x -= dx
                screen_scroll = -dx

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
    def __init__(self, x, y, scale, speed, char_type="enemy", pers_type="officer"):
        super().__init__(x, y, scale, speed)
        self.char_type = char_type
        self.pers_type = pers_type
        self.health = 100
        self.ammo = 1000
        self.shoot_cooldown = 0
        self.animation_list = []
        #ai
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20) #150 - how far enemies can look
        

        
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
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 100) == 10:
                self.update_action(0) #idling
                self.idling = True
                self.idling_counter = random.randint(20, 50)
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
        self.rect.x += screen_scroll
        
        
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
                    if tile >= 0 and tile <= 16: 
                        self.obstacle_list.append(tile_data)
                    elif 17 <= tile <= 36:
                        self.decoration_list.append(tile_data)
                    elif tile == 37:
                        player = MainCharacter(x * TILE_SIZE, y * TILE_SIZE, 1.5, 5, 20) #(x, y, scale, speed. ammo)
                        healthbar = HealthBar(10, 10, player.health, player.max_health)
                        self.player = player
                        self.healthbar = healthbar
                    elif tile == 38:
                        enemy = Enemy(x * TILE_SIZE, y * TILE_SIZE, 2, 3)
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
        

        return player, healthbar

    def draw(self):
        for tile in self.decoration_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
        
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])



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
        
    def update(self):
        #map scroll update
        self.rect.x += screen_scroll
        
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



class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
         
    def draw(self, health):
        #update with new health
        self.health = health
        #health ratio - diference between full health and actual health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))




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
                print("Player dostal")
                player.update_action(5)
                player.health -= 5
                self.kill()
        for enemy in enemy_group:        
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if isinstance(self.shooter, Enemy):
                    print("bot nie dostal, a mogl dostac")
                    pass
                elif enemy.alive:
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
        self.rect.x += dx + screen_scroll
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

        
        
#create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
# decoration_group = pygame.sprite.Group()
# exit_group = pygame.sprite.Group()




# player = MainCharacter(200, 250, 2, 5, 20) #(x, y, scale, speed)
# healthbar = HealthBar(10, 10, player.health, player.max_health)



world = World(img_list, 'level3_przeszkody.csv')

player = world.player
healthbar = world.healthbar


run = True
while run:
    
    clock.tick(FPS)
    
    #update background
    draw_bg()
    #draw world map
    world.draw()
    #player health
    # healthbar.draw(player.health)
    
    #show ammo
    # draw_text('AMMO: ', font, WHITE, 10, 35)
    # if player.ammo <= 20:      
    #     for x in range(player.ammo):
    #         screen.blit(bullet_img, (90 + (x * 10), 40))
    # else:
    #     rest_ammo = player.ammo - 20
    #     for x in range(20):
    #         screen.blit(bullet_img, (90 + (x * 10), 40))
    #     for y in range(rest_ammo):
    #         screen.blit(bullet_img, (90 + (y * 10), 30))
                
    # #show grenades
    # draw_text(f'GRENADE: {player.grenades}', font, WHITE, 10, 60)
    # for x in range(player.grenades):
    #     screen.blit(grenade_img, (135 + (x * 15), 60))
    # #show money
    # draw_text(f'MONEY: {player.money}', font, WHITE, 10, 85)
    
    
    
    player.update()
    player.draw()
    
    
    for enemy in enemy_group:
        enemy.ai()
        enemy.update()
        enemy.draw()
    
    #update and draw groups
    bullet_group.update()
    grenade_group.update()
    item_box_group.update()
    explosion_group.update()
    # decoration_group.update()
    # exit_group.update()
    
    bullet_group.draw(screen)
    grenade_group.draw(screen)
    item_box_group.draw(screen)
    explosion_group.draw(screen)
    # decoration_group.draw(screen)
    # exit_group.draw(screen)
    
    #update player actions
    if player.alive:
        #shoot
        if shoot:
            player.shoot()
            player.update_action(4)
        #grenades
        elif grenade and grenade_thrown == False and player.grenades > 0:
            grenade = Grenade(player.rect.centerx + int(0.95 * player.rect.size[0] * player.direction),\
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
        screen_scroll = player.move(moving_left, moving_right)
        bg_scroll -= screen_scroll
    
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
