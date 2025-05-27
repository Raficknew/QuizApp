import pygame

from abc import ABC, abstractmethod

class Object(ABC):

    @abstractmethod
    def isClicked(self,event):
        pass

    @abstractmethod
    def drawObject(self,screen):
        pass


class Background(Object):

    def __init__(self, x, y, width, height, backgroundColor):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.backgroundColor = backgroundColor
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.x, self.y)
        
    def drawObject(self, screen):
        pygame.draw.rect(screen, self.backgroundColor , self.rect)
    
    def isClicked(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False