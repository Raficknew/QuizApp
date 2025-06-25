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
       self._questionTitle = questionTitle
       self._answers = answers
       self._answer = answer

   @property
   def answer(self):
       return self._answer

   @property
   def questionTitle(self):
       return self._questionTitle

   @property
   def answers(self):
       return self._answers

   def setQuestion(self,newQuestionTitle,newAnswer,newAnswers):
       self._answer = newAnswer
       self._questionTitle = newQuestionTitle
       self._answers = newAnswers

   def __str__(self):
        return f"{self.questionTitle}, {self.answers}, {self.answer}"


class ChangeQuestion(Command):

    questionHistory = []
    
    
    def __init__(self,question,newQuestionTitle,newAnswer,newAnswers):
        self.question = question
        self.newQuestionTitle = newQuestionTitle
        self.newAnswer = newAnswer
        self.newAnswers = newAnswers
    
    def execute(self):

        ChangeQuestion.questionHistory.append((self.question.questionTitle,self.question.answers,self.question.answer))
        self.question.setQuestion(self.newQuestionTitle,self.newAnswer,self.newAnswers)
    
    def __str__(self):
        return f"{ChangeQuestion.questionHistory}"


class QuestionScreen(Setup):

    correctQuestions = 0

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

        

    @staticmethod
    def randomQuestion(questions):

        element = choice(questions)
        questions.remove(element)
        return element

    def drawQuestionScreen(self):

        for object in self.objects:
            object.drawWithText(self.screen)

    def newQuestion(self):

        newQuestion = self.randomQuestion(self.questions)
        ChangeQuestion(self.currentQuestion,newQuestion[0],newQuestion[-1],newQuestion[1:-1]).execute() 
        self.header.updateText(self.currentQuestion.questionTitle)

    def changeQuestionScreen(self,event):

        if event is None:
            self.newQuestion()
            for button, j in zip(self.buttons, range(4)):
                button.updateText(self.currentQuestion.answers[j])
            return
 

        for button in self.objects:
            if button.isClicked(event):
                if button.text == self.currentQuestion.answer:
                    QuestionScreen.correctQuestions += 1
                self.newQuestion()
                for button, j in zip(self.buttons, range(4)):
                    button.updateText(self.currentQuestion.answers[j])
                break
    
        

class Screen(Setup):

    currentScreen = "start"
    

    def __init__(self,questions):

        super().__init__()
        self.startButton = Rect_Button(640,350,self.buttonWidth,self.buttonHeight,'start',self.font,self.fontColor , self.backgroundColor)
        self.questionScreen = QuestionScreen(questions)
        self.questions = questions
        self.screen.fill("teal") 
        self.startTime = pygame.time.get_ticks()
        self.questionDuration = 31000
        

    def handle(self,event):

        elapsedTime = pygame.time.get_ticks() - self.startTime

        if Screen.currentScreen == 'start':
            self.screen.fill("teal")
            self.startButton.drawWithText(self.screen)
            pygame.display.flip()
            if self.startButton.isClicked(event):
                Screen.currentScreen = 'questions'
            
        elif Screen.currentScreen == 'questions' and len(ChangeQuestion.questionHistory) != 19:
            remainingTime = max(0, (self.questionDuration - elapsedTime) // 1000)
            timerText = self.font.render(f"Czas: {remainingTime}", True, (255, 0, 0))
            correct = self.font.render(str(QuestionScreen.correctQuestions),1,self.fontColor,None)
            
            self.screen.fill("teal")
            self.screen.blit(timerText, (500, 0))
            self.screen.blit(correct,(0,0),None)
            self.questionScreen.drawQuestionScreen()
            pygame.display.flip()

            if event is not None and event.type == pygame.MOUSEBUTTONDOWN:
                self.questionScreen.changeQuestionScreen(event)
                self.startTime = pygame.time.get_ticks()


            if elapsedTime >= self.questionDuration:
                self.questionScreen.changeQuestionScreen(None)  
                self.startTime = pygame.time.get_ticks()

        else:
            self.screen.fill("teal")
            text = self.font.render(f"{QuestionScreen.correctQuestions}/20", True, (255, 255, 255))
            self.screen.blit(text, (100, 200))
            pygame.display.flip()
            
                

        