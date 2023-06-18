import pygame

class Button:
    def __init__(self, x, y, image, scale=1):
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))  # Przeskalowanie obrazka
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        # Rysuje obraz na podanym powierzchni
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def is_clicked(self, event):
        # Zwraca True jeśli przycisk został kliknięty
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                return True
        return False
