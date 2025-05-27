import pygame

from classes.background import Background

class Rect_Button(Background):

    def __init__(self, x, y, width, height, text, textFont, textColor,backgroundColor):
        super().__init__(x, y, width, height, backgroundColor)
        self.text = text
        self.textColor = textColor
        self.textFont = textFont
        self.textSurface = self.textFont.render(self.text, True, self.textColor)
        self.textRect = self.textSurface.get_rect(center=self.rect.center)

    def drawWithText(self,screen):
        self.drawObject(screen)
        self.textRect.center = self.rect.center
        screen.blit(self.textSurface, self.textRect)

    def updateText(self, new_text):
        self.text = new_text
        self.textSurface = self.textFont.render(self.text, True, self.textColor)
        self.textRect = self.textSurface.get_rect(center=self.rect.center)




