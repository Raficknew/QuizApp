import pygame
from components.changingscreen import  Screen

q = []
with open('all_questions/questions0.txt','r',encoding='utf-8') as data:
    questions = data.read()
    questions = questions.split('\n')
    for question in questions:
        q.append(question.split('|'))
    

       
pygame.init()

running = True

game = Screen(q)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        game.handle(event)
        