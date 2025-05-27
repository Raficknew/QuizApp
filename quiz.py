import pygame
from components.button import Rect_Button
from components.questionHeader import QuestionHeader

class Question():
   def __init__(self, questionTitle, answers, answer):
       self.questionTitle = questionTitle
       self.answers = answers
       self.answer = answer

pygame.init()
screen = pygame.display.set_mode((1280, 760))
font = pygame.font.SysFont("Arial", 36)
font_color = "black"
backgroundColor = (255,255,255)
buttonWidth = 700
buttonHeight = 100
running = True

answers = []
question = Question("Jaki jest największy ocean na Ziemi?",["Ocean Atlantycki","Ocean Indyjski","Ocean Arktyczny","Ocean Spokojny"],"Ocean Spokojny")

header = QuestionHeader(640,100,buttonWidth,buttonHeight,question.questionTitle,font,font_color ,backgroundColor)
b1 = Rect_Button(640,350,buttonWidth,buttonHeight,question.answers[0],font,font_color ,backgroundColor)
b2 = Rect_Button(640,460,buttonWidth,buttonHeight,question.answers[1],font,font_color ,backgroundColor)
b3 = Rect_Button(640,570,buttonWidth,buttonHeight,question.answers[2],font,font_color ,backgroundColor)
b4 = Rect_Button(640,680,buttonWidth,buttonHeight,question.answers[3],font,font_color ,backgroundColor)

def checkIfAnswerIsCorrect(answer):
    if answer == question.answer:
        return True
    else:
        return False

def handleNextQuestion():
    header.updateText("xddd")
    b1.updateText("test1")
    b2.updateText("test2")
    b3.updateText("test3")
    b4.updateText("test4")

def handleQuestionChange(answer):

    answers.append(checkIfAnswerIsCorrect(answer))
    handleNextQuestion()
    print(answers)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if b1.isClicked(event):
            handleQuestionChange(b1.text)
        if b2.isClicked(event):
            handleQuestionChange(b2.text)
        if b3.isClicked(event):
            handleQuestionChange(b3.text)
        if b4.isClicked(event):
            handleQuestionChange(b4.text)

    screen.fill("teal")

    b1.drawWithText(screen)
    b2.drawWithText(screen)
    b3.drawWithText(screen)
    b4.drawWithText(screen)
    header.drawWithText(screen)

    pygame.display.flip()