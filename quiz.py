import pygame

from classes.quiz import RandomQuiz
from components.changingscreen import Screen

pygame.init()

running = True

quiz = RandomQuiz()
quiz.run()
questions = quiz.get_questions()

game = Screen(questions)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        game.handle(event)
    game.handle(None)
