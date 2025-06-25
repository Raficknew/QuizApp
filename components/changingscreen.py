from classes.question import QuestionScreen, ChangeQuestion
from classes.setup import Setup
from components.button import Rect_Button
import pygame

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
            
                

        