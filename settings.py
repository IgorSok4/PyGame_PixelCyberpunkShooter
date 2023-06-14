import pygame

SCREENSIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 672

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('PixelCyberpunk')



#game variables
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 21
COLS = 96
TILE_SIZE = 32
TILE_TYPES = 42
level = 1
screen_scroll = 0



    
bullet_img = pygame.image.load('media/bullet/ak.png')
bullet_img_rotated = pygame.transform.rotate(bullet_img, -90)
grenade_img = pygame.image.load('media/other/grenade/idle/0.png')
grenade_img = pygame.transform.scale(grenade_img, (grenade_img.get_width() * 1.5, grenade_img.get_height() * 1.5))
money_img = pygame.image.load('media/other/money/0.png')
money_img = pygame.transform.scale(money_img, (money_img.get_width() * 0.8, money_img.get_height() * 0.8))
background = pygame.image.load('media/map/level1/level4.png')


#define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)