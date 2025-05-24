import pygame

class Background():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, width, height)

    def draw(self, screen):
        self.rect.center = (self.x, self.y)
        pygame.draw.rect(screen, self.color, self.rect)