import pygame
import glob


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

#set framerate
clock = pygame.time.Clock()
FPS = 60

# define player actions variables
moving_left = False
moving_right = False

#define colours
BG = (144, 201, 120)


def draw_bg():
    screen.fill(BG)






class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, char_type, pers_type, pose_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.pers_type = pers_type
        self.pose_type = pose_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
       
        # count amount of images in folder
        folder_path = f'media/{self.char_type}/{self.pers_type}/{self.pose_type}'
        file_count = len(glob.glob(folder_path + '/*'))
        
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'media/{self.char_type}/{self.pers_type}/{self.pose_type}/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
            
        temp_list = []
        for i in range(6):
            img = pygame.image.load(f'media/{self.char_type}/{self.pers_type}/walk/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  


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

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy
        
        
    def update_animation(self):
        ANIMATION_COOLDOWN = 150
        #update image depeding on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enought time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # index error fix
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        
        
        

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


player = MainCharacter('enemy', 'officer', 'idle', 200, 200, 3, 5)
# enemy = MainCharacter('enemy', 'officer', 'idle', 400, 200, 3, 5)



run = True
while run:
    
    clock.tick(FPS)
    
    draw_bg()
    
    player.update_animation()
    player.draw()
    # enemy.draw()
    
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
            if event.key == pygame.K_ESCAPE:
                run = False

             
        #keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            


    pygame.display.update()

pygame.quit()
