import pygame

class Text:
    def __init__(self, value, text_colour, px, py, font_type='impact', font_size=74):
        self.value = value
        self.text_colour = text_colour
        self.px = px
        self.py = py
        self.font_type = font_type
        self.font_size = font_size

    def draw(self, screen):
        font = pygame.font.SysFont(self.font_type, self.font_size)
        text = str(self.value)
        image = font.render(text, True, self.text_colour)
        rect = image.get_rect()
        rect.center = self.px, self.py
        screen.blit(image, rect)
        
    def update(self, new_value):
        self.value = new_value
