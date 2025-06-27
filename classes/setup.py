import pygame

class Setup():

    def __init__(self):

        self.screen = pygame.display.set_mode((1280, 760))
        self.font = pygame.font.SysFont("Arial", 30)
        self.fontColor = "black"
        self.backgroundColor = (255, 255, 255)
        self.buttonWidth = 700
        self.buttonHeight = 100
