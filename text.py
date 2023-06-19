import pygame

class Text:
    def __init__(self, text, text_colour, px, py, font_type='impact', font_size=24):
        self.text = str(text)
        font = pygame.font.SysFont(font_type, font_size)
        self.image = font.render(self.text, True, text_colour)
        self.rect = self.image.get_rect()
        self.rect.center = px, py

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def update(self, new_value, text_colour, font_type='impact', font_size=24):
        self.text = str(new_value)
        font = pygame.font.SysFont(font_type, font_size)
        self.image = font.render(self.text, True, text_colour)

