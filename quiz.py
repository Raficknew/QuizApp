import pygame

class Button():
    def __init__(self,x,y,width,height,color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.x,self.y,width,height)
        
    def draw(self,screen):
        self.rect.center = (self.x,self.y)
        pygame.draw.rect(screen,self.color,self.rect)
    
    def isclicked(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
class Button_with_text(Button):
    def __init__(self,x,y,width,height,text,font,font_color,color):
        super().__init__(x,y,width,height,color)
        self.text = text
        self.font = font
        self.font_color = font_color
        self.text_surface = self.font.render(self.text,True,self.font_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        
    def draw(self, screen):
        super().draw(screen)
        self.text_rect.center = self.rect.center
        screen.blit(self.text_surface,self.text_rect)
'''
class Button_grid(Button_with_text): przyklad dziedziczenia wielopoziomowego ale nw czy ma sens
    pass
te klasy będą do podszlifowania bo ucze sie na bieżąco i pygame i tworzenia obiektów
button grid na takiej zasadzie ze tworzy juz siatke obiektów, 4 przyciski
'''
pygame.init()
screen = pygame.display.set_mode((1280, 760))
font = pygame.font.SysFont("Arial", 36) 
running = True
while running:
    b1 = Button_with_text(100,100,100,100,'sigma',font,(0,0,0),(255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if b1.isclicked(event) == True:
            print('Click')
    screen.fill((0, 0, 0))
    b1.draw(screen)
    pygame.display.flip()