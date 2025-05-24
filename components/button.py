import pygame

from classes.background import Background

class Button(Background):
    def isclicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class Button_with_text(Button):
    def __init__(self, x, y, width, height, text, font, font_color, color):
        super().__init__(x, y, width, height, color)
        self.text = text
        self.font = font
        self.font_color = font_color
        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        super().draw(screen)
        self.text_rect.center = self.rect.center
        screen.blit(self.text_surface, self.text_rect)

    def update_text(self, new_text):
        self.text = new_text
        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)



'''
class Button_grid(Button_with_text): przyklad dziedziczenia wielopoziomowego ale nw czy ma sens
    pass
te klasy będą do podszlifowania bo ucze sie na bieżąco i pygame i tworzenia obiektów
button grid na takiej zasadzie ze tworzy juz siatke obiektów, 4 przyciski
'''