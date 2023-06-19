import pygame

from settings import *
from text import Text
from groups import *
from grenade import Grenade
from static_objects import *
from globals import g
from button import Button


pygame.init()


def draw_bg(bg_scroll):
    screen.fill(BLACK)
    width = background.get_width()
    for x in range(2):
        screen.blit(background, ((x * width) - bg_scroll * 1, 0))
        
def draw_menu_bg(menu_bg_scroll):
    screen.fill(BLACK)
    width = menu_background_1.get_width()
    for x in range(5):
        screen.blit(menu_background_1, ((x * width) - menu_bg_scroll * 0.5, 0))
        screen.blit(menu_background_2, ((x * width) - menu_bg_scroll * 0.8, SCREEN_HEIGHT - menu_background_2.get_height()))
        screen.blit(menu_background_3, ((x * width) - menu_bg_scroll * 1, SCREEN_HEIGHT - menu_background_3.get_height()))
        screen.blit(menu_background_4, ((x * width) - menu_bg_scroll * 1.5, SCREEN_HEIGHT - menu_background_4.get_height()))

# #reset level
def reset_level():
    global world, player, healthbar
    # Reset object groups
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    
    # new_world = world.load_map('level3_przeszkody.csv')
    # print(f'id(player) reset_level: {id(player)}')
    world, player, healthbar = reset_static_objects()



def main():
    
    clock = pygame.time.Clock()
    FPS = 60
    
    # define player actions variables
    moving_left = False
    moving_right = False
    shoot = False
    grenade = False
    grenade_thrown = False
    bg_scroll = 0
    start_game = False
    menu_state = "main"

    #buttons
    start_button = Button(100, 100, menu_button_start, 2)
    quit_button = Button(100, 200, menu_button_quit, 2)
    level_1_button = Button(100, 100, menu_button_level_1, 2)
    level_2_button = Button(100, 200, menu_button_level_2, 2)
    level_3_button = Button(100, 300, menu_button_level_3, 2)
    return_button = Button(10, 10, menu_button_return, 1)
    level_retry_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, retry_button, 3)
    text_points = Text(player, BLACK, 60, 118, font_size=24)

    run = True
    while run:
        
        clock.tick(FPS)
        # print(f'id(player: {id(player)}')
        if start_game == False:
            if menu_state == 'main':
                g.bg_scroll_menu += 2
                draw_menu_bg(g.bg_scroll_menu)
                start_button.draw(screen)
                quit_button.draw(screen)
                for event in pygame.event.get():
                    if start_button.is_clicked(event):
                        # start_game = True
                        menu_state = 'level'
                    if quit_button.is_clicked(event):
                        run = False
            if menu_state == 'level':
                g.bg_scroll_menu += 2
                draw_menu_bg(g.bg_scroll_menu)
                return_button.draw(screen)
                level_1_button.draw(screen)
                level_2_button.draw(screen)
                level_3_button.draw(screen)
                for event in pygame.event.get():
                    if return_button.is_clicked(event):
                        menu_state = 'main'
                    if level_1_button.is_clicked(event):
                        g.level = 1
                        reset_level()
                        start_game = True
                    if level_2_button.is_clicked(event):
                        g.level = 2
                        reset_level()
                        start_game = True
                    if level_3_button.is_clicked(event):
                        g.level = 3
                        reset_level()
                        start_game = True
        else:
        
        
            #update background
            draw_bg(bg_scroll)
            #draw world map
            world.draw()
            #player
            player.update()
            player.draw()
            #player health
            healthbar.draw(player.health)


            #enemies
            for enemy in enemy_group:
                enemy.ai()
                enemy.update()
                enemy.draw()
            
            # show ammo
            if player.ammo <= 20:      
                for x in range(player.ammo):
                    screen.blit(bullet_img_rotated, (10 + (x * 5), 70))
            else:
                rest_ammo = player.ammo - 20
                for x in range(20):
                    screen.blit(bullet_img_rotated, (10 + (x * 5), 70))
                for y in range(rest_ammo):
                    screen.blit(bullet_img_rotated, (10 + (y * 5), 80))
                        
            #show grenades
            for x in range(player.grenades):
                screen.blit(grenade_img, (135 + (x * 15), 60))
            #show money
            screen.blit(money_img, (10, 100))
            text_points.draw(screen)

            
            #update and draw groups
            bullet_group.update()
            grenade_group.update()
            item_box_group.update()
            explosion_group.update()
            
            bullet_group.draw(screen)
            grenade_group.draw(screen)
            item_box_group.draw(screen)
            explosion_group.draw(screen)
            
            
            #check for level exit
            for tile in world.decoration_list:
                if isinstance(tile, pygame.Rect):
                    if player.rect.colliderect(tile):
                        reset_level()
                        start_game = False

            
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
                
                g.screen_scroll = player.move(moving_left, moving_right)
                bg_scroll -= g.screen_scroll
            else:
                if level_retry_button.draw(screen):
                    g.screen_scroll = 0
                    bg_scroll = 0
        
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
                    
            if level_retry_button.is_clicked(event):
                g.screen_scroll = 0
                bg_scroll = 0
                start_game = False
                reset_level()
                

                


        pygame.display.update()

    pygame.quit()
    

if __name__ == "__main__":
    main()