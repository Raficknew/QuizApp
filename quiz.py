import pygame
from components.button import Button_with_text
from components.questionHeader import QuestionHeader

class Question():
   def __init__(self, questionTitle, answers, answer):
       self.questionTitle = questionTitle
       self.answers = answers
       self.answer = answer

pygame.init()
screen = pygame.display.set_mode((1280, 760))
font = pygame.font.SysFont("Arial", 36)
running = True

answers = []
question = Question("Jaki jest największy ocean na Ziemi?",["Ocean Atlantycki","Ocean Indyjski","Ocean Arktyczny","Ocean Spokojny"],"Ocean Spokojny")

header = QuestionHeader(640,100,600,100,question.questionTitle,font,"black",(255,255,255))
b1 = Button_with_text(640,350,600,100,question.answers[0],font,"black",(255,255,255))
b2 = Button_with_text(640,460,600,100,question.answers[1],font,"black",(255,255,255))
b3 = Button_with_text(640,570,600,100,question.answers[2],font,"black",(255,255,255))
b4 = Button_with_text(640,680,600,100,question.answers[3],font,"black",(255,255,255))

def checkIfAnswerIsCorrect(answer):
    if answer == question.answer:
        return True
    else:
        return False

def handleNextQuestion():
    header.update_text("xddd")
    b1.update_text("test1")
    b2.update_text("test2")
    b3.update_text("test3")
    b4.update_text("test4")

def handleQuestionChange(answer):

    answers.append(checkIfAnswerIsCorrect(answer))
    handleNextQuestion()
    print(answers)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if b1.isclicked(event):
            handleQuestionChange(b1.text)
        if b2.isclicked(event):
            handleQuestionChange(b2.text)
        if b3.isclicked(event):
            handleQuestionChange(b3.text)
        if b4.isclicked(event):
            handleQuestionChange(b4.text)

    screen.fill("teal")

    b1.draw(screen)
    b2.draw(screen)
    b3.draw(screen)
    b4.draw(screen)
    header.draw(screen)

    pygame.display.flip()