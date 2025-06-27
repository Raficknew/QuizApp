import pygame

from classes.quiz import RandomQuiz
from components.changingscreen import Screen



pygame.init()

running = True

quiz = RandomQuiz('all_questions/OOP_quiz.txt')
quiz.run()

game = Screen(quiz.questions)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        game.handle(event)
    game.handle(None)
