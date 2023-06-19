import pygame
from pygame import mixer
from globals import g

mixer.init()

SCREENSIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 672

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('PixelCyberpunk')



#game variables
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 22
COLS = 96
TILE_SIZE = 32
TILE_TYPES = 47
# level = 1
screen_scroll = 0




    
bullet_img = pygame.image.load('media/bullet/ak.png')
bullet_img_rotated = pygame.transform.rotate(bullet_img, -90)
bullet_enemy = pygame.image.load('media/bullet/blaster.png')
grenade_img = pygame.image.load('media/other/grenade/idle/0.png')
grenade_img = pygame.transform.scale(grenade_img, (grenade_img.get_width() * 1.5, grenade_img.get_height() * 1.5))
money_img = pygame.image.load('media/other/money/0.png')
money_img = pygame.transform.scale(money_img, (money_img.get_width() * 0.8, money_img.get_height() * 0.8))

exit_sign = pygame.image.load('media/map/level1/tiles/43.png')

# menu background
menu_background_1 =  pygame.image.load('media/map/menu/background/background_1.png')
menu_background_2 =  pygame.image.load('media/map/menu/background/background_2.png')
menu_background_3 =  pygame.image.load('media/map/menu/background/background_3.png')
menu_background_4 =  pygame.image.load('media/map/menu/background/background_4.png')

# menu buttons
menu_button_start = pygame.image.load('media/map/menu/buttons/button_start.png')
menu_button_quit = pygame.image.load('media/map/menu/buttons/button_quit.png')
menu_button_level_1 = pygame.image.load('media/map/menu/buttons/button_level_1.png')
menu_button_level_2 = pygame.image.load('media/map/menu/buttons/button_level_2.png')
menu_button_level_3 = pygame.image.load('media/map/menu/buttons/button_level_3.png')
menu_button_return = pygame.image.load('media/map/menu/buttons/button_return.png')
menu_button_sound_on = pygame.image.load('media/map/menu/buttons/sound_on.png')
menu_button_sound_off = pygame.image.load('media/map/menu/buttons/sound_off.png')

#level buttons
retry_button = pygame.image.load('media/map/level_buttons/retry.png')

#music mand sounds
pygame.mixer.music.load('media/sounds/menu_music.mp3')
pygame.mixer.music.set_volume(0.1)
# pygame.mixer.music.load('media/sounds/biker_rifle_shoot_sound.mp3')
# pygame.mixer.music.load('media/sounds/officer_rifle_shoot_sound.mp3')
biker_shoot_sound = pygame.mixer.Sound('media/sounds/biker_rifle_shoot_sound.mp3')
biker_shoot_sound.set_volume(0.1)
officer_shoot_sound = pygame.mixer.Sound('media/sounds/officer_rifle_shoot_sound.mp3')
officer_shoot_sound.set_volume(0.2)
boss_shoot_sound = pygame.mixer.Sound('media/sounds/boss_shoot_sound.mp3')
boss_shoot_sound.set_volume(0.5)
grenade_explosion_sound = pygame.mixer.Sound('media/sounds/grenade_explosion.mp3')
grenade_explosion_sound.set_volume(0.3)
biker_walk_sound = pygame.mixer.Sound('media/sounds/biker_walk.mp3')
biker_walk_sound.set_volume(10)
biker_reload_sound = pygame.mixer.Sound('media/sounds/biker_reload.mp3')
biker_reload_sound.set_volume(0.2)
biker_empty_mag_sound = pygame.mixer.Sound('media/sounds/biker_empty_mag.mp3')
biker_empty_mag_sound.set_volume(0.2)
item_pickup_sound = pygame.mixer.Sound('media/sounds/item_pickup_sound.mp3')
item_pickup_sound.set_volume(0.5)

#define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (40,35,49)