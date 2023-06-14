import pygame

from settings import *

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
        self.image = pygame.image.load(f'media/other/health_bar.png') 
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.bar_width = 152
        self.bar_height = 4


    def draw(self, health):
        screen.blit(self.image, self.rect)
        self.health = health
        health_ratio = self.health / self.max_health
        # health bar during game
        current_bar_width = self.bar_width * health_ratio
        health_bar_topleft = (self.rect.left + 35, self.rect.top + 30)
        health_bar_rect = pygame.Rect(health_bar_topleft,(current_bar_width,self.bar_height))
        pygame.draw.rect(screen, RED, health_bar_rect)
        
