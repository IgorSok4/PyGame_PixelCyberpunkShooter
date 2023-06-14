import pygame

from settings import *
from text import Text
from groups import *
from grenade import Grenade
from static_objects import *
from globals import g

pygame.init()


def draw_bg(bg_scroll):
    screen.fill(BLACK)
    width = background.get_width()
    for x in range(2):
        screen.blit(background, ((x * width) - bg_scroll * 1, 0))


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

    
    
    text_points = Text(player, BLACK, 60, 118, font_size=24)

    run = True
    while run:
        
        clock.tick(FPS)
        #update background
        draw_bg(bg_scroll)
        #draw world map
        world.draw()
        #player health
        healthbar.draw(player.health)
        
        # # show ammo
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
                    
        #show grenades
        for x in range(player.grenades):
            screen.blit(grenade_img, (135 + (x * 15), 60))
        #show money
        screen.blit(money_img, (10, 100))
        text_points.draw(screen)
        
        
        
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
        global screen_scroll
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
    

if __name__ == "__main__":
    main()