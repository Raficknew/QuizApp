from abc import ABC, abstractmethod
from components.button import Rect_Button
from components.questionHeader import QuestionHeader
import pygame
from random import choice

class Setup():

    def __init__(self):

        self.screen = pygame.display.set_mode((1280, 760))
        self.font = pygame.font.SysFont("Arial", 36)
        self.fontColor = "black"
        self.backgroundColor = (255, 255, 255)
        self.buttonWidth = 700
        self.buttonHeight = 100

class Command(ABC):

    @abstractmethod
    def execute(self):
        pass


class Question():
   
   def __init__(self, questionTitle, answers, answer):
       self.questionTitle = questionTitle
       self.answers = answers
       self.answer = answer

   def setQuestion(self,newQuestionTitle,newAnswer,newAnswers):
       self.answer = newAnswer
       self.questionTitle = newQuestionTitle
       self.answers = newAnswers

   def __str__(self):
        return f"{self.questionTitle}, {self.answers}, {self.answer}"


class ChangeQuestion(Command):

    allQuestions = []
    
    
    def __init__(self,question,newQuestionTitle,newAnswer,newAnswers):
        self.question = question
        self.newQuestionTitle = newQuestionTitle
        self.newAnswer = newAnswer
        self.newAnswers = newAnswers
    
    def execute(self):

        ChangeQuestion.allQuestions.append(self.question)
        self.question.setQuestion(self.newQuestionTitle,self.newAnswer,self.newAnswers)

class RedrawButton(Command):

    allButtons = []

    def __init__(self,button,newText):
        self.button = button
        self.newText = newText

    def execute(self):
        RedrawButton.allButtons.append(self.button)
        self.button.updateText(self.newText)

    '''
    def undo(self):
        if RedrawButton.allButtons:
            lastButton = RedrawButton.allButtons.pop() ---> nie będzie działać z tym w jaki sposób zaciągam pytania
            lastButton.drawWithText()
    '''

class QuestionScreen(Setup):

    def __init__(self, questions):

        super().__init__()
        self.questions = questions
        self.firstRandomQuestion = choice(questions)
        self.currentQuestion = Question(self.firstRandomQuestion[0], self.firstRandomQuestion[1:-1], self.firstRandomQuestion[-1])
        self.questions.remove(self.firstRandomQuestion)
        self.b1 = Rect_Button(640, 250, self.buttonWidth, self.buttonHeight, self.currentQuestion.answers[0], self.font, self.fontColor, self.backgroundColor)
        self.b2 = Rect_Button(640, 370, self.buttonWidth, self.buttonHeight, self.currentQuestion.answers[1], self.font, self.fontColor, self.backgroundColor)
        self.b3 = Rect_Button(640, 490, self.buttonWidth, self.buttonHeight, self.currentQuestion.answers[2], self.font, self.fontColor, self.backgroundColor)
        self.b4 = Rect_Button(640, 610, self.buttonWidth, self.buttonHeight, self.currentQuestion.answers[3], self.font, self.fontColor, self.backgroundColor)
        self.buttons = [self.b1, self.b2, self.b3, self.b4]
        self.header = QuestionHeader(640,100,self.buttonWidth,self.buttonHeight,self.currentQuestion.questionTitle,self.font,self.fontColor , self.backgroundColor)
        self.objects = self.buttons + [self.header]
        #self.commandHistory = []
        

    @staticmethod
    def randomQuestion(questions):

        element = choice(questions)
        questions.remove(element)
        return element

    def drawQuestionScreen(self):

        for object in self.objects:
            object.drawWithText(self.screen)


    def changeQuestionScreen(self,event):

        for button in self.objects:
            if button.isClicked(event):
                  
                newQuestion = self.randomQuestion(self.questions)
                self.header.updateText(self.currentQuestion.questionTitle)
                ChangeQuestion(self.currentQuestion,newQuestion[0],newQuestion[-1],newQuestion[1:-1]).execute() #kwestia do przemyslenia czy nadpisywać pytanie
                for button, j in zip(self.buttons, range(4)):
                    RedrawButton(button, self.currentQuestion.answers[j]).execute() #później poprzez historie komend można zrobić wracanie do pytań

class Screen(Setup):

    currentScreen = "start"
    

    def __init__(self,questions):

        super().__init__()
        self.startButton = Rect_Button(640,350,self.buttonWidth,self.buttonHeight,'start',self.font,self.fontColor , self.backgroundColor)
        self.questionScreen = QuestionScreen(questions)
        self.questions = questions
        self.screen.fill("teal") 
        

    def handle(self,event):

        if Screen.currentScreen == 'start':
            self.screen.fill("teal")
            self.startButton.drawWithText(self.screen)
            pygame.display.flip()
            if self.startButton.isClicked(event):
                Screen.currentScreen = 'questions'
            
        elif Screen.currentScreen == 'questions' and len(ChangeQuestion.allQuestions) != 19:
            self.screen.fill("teal") 
            self.questionScreen.drawQuestionScreen()
            pygame.display.flip()
            if event:
                self.questionScreen.changeQuestionScreen(event)
        else:
            self.screen.fill("teal")
            text = self.font.render("Sigma!", True, (255, 255, 255))
            self.screen.blit(text, (100, 200))
            pygame.display.flip()
            
                

        