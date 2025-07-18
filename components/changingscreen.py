from abc import ABC, abstractmethod

from classes.question import QuestionScreen, ChangeQuestion
from classes.setup import Setup
from components.button import Rect_Button
from classes.question import QuestionHeader
import pygame
from random import choice
from classes.quiz import RandomQuiz
import time

class ErrorDodawaniaPytan(Exception):
    pass

class Screen(Setup):
    currentScreen = "menu"
    
    def __init__(self, questions):
        super().__init__()
        self.questions = questions
        self.questionScreen = QuestionScreen(questions)
        self.startButton = Rect_Button(640, 300, self.buttonWidth, self.buttonHeight, 'Start', self.font, self.fontColor, self.backgroundColor)
        self.goToAddQuestionButton = Rect_Button(640, 420, self.buttonWidth, self.buttonHeight, 'Dodaj pytanie', self.font, self.fontColor, self.backgroundColor)
        self.chooseQuizButton = Rect_Button(640, 540, self.buttonWidth, self.buttonHeight, 'Wybierz zestaw pytań', self.font, self.fontColor, self.backgroundColor)
        self.newQuestion = ''
        self.newAnswers = ['', '', '', '']
        self.correctAnswer = ''
        self.inputBoxes = [
            pygame.Rect(300, 100, 680, 60),
            pygame.Rect(300, 200, 320, 60),
            pygame.Rect(660, 200, 320, 60),
            pygame.Rect(300, 300, 320, 60),
            pygame.Rect(660, 300, 320, 60),
            pygame.Rect(300, 400, 680, 60),
        ]
        self.activeInput = None
        self.addQuestionButton = Rect_Button(640, 550, 300, 70, 'Dodaj pytanie', self.font, self.fontColor, self.backgroundColor)
        self.backButton = Rect_Button(640, 640, 300, 70, 'Powrót', self.font, self.fontColor, self.backgroundColor)
        self.menuButtons = [self.chooseQuizButton,self.goToAddQuestionButton,self.startButton]
        self.startTime = pygame.time.get_ticks()
        self.questionDuration = 31000
        self.currentQuizFile = "all_questions/OOP_quiz.txt"
        self.waitingForNextQuestion = False
        self.answerShownTime = 0
        self.answerDisplayDuration = 1000

    def handle(self, event):
        elapsedTime = pygame.time.get_ticks() - self.startTime

        if Screen.currentScreen == "menu":
            self.screen.fill("teal")
            for i in self.menuButtons:
                i.drawWithText(self.screen)
            pygame.display.flip()
            if event is not None and event.type == pygame.MOUSEBUTTONDOWN:
                if self.startButton.isClicked(event):
                    Screen.currentScreen = "questions"
                    self.startTime = pygame.time.get_ticks()
                elif self.goToAddQuestionButton.isClicked(event):
                    Screen.currentScreen = "add_question"
                elif self.chooseQuizButton.isClicked(event):
                    Screen.currentScreen = "choose_quiz"
        

        elif Screen.currentScreen == "add_question":
            self.screen.fill("teal")

            labels = ['Pytanie:', 'Odpowiedź 1:', 'Odpowiedź 2:', 'Odpowiedź 3:', 'Odpowiedź 4:', 'Poprawna odpowiedź:']
            for i, box in enumerate(self.inputBoxes):
                pygame.draw.rect(self.screen, (0, 0, 0), box, 2)
                text = ''
                if i == 0:
                    text = self.newQuestion
                elif 1 <= i <= 4:
                    text = self.newAnswers[i - 1]
                elif i == 5:
                    text = self.correctAnswer
                txt_surface = self.font.render(text, True, (0, 0, 0))
                self.screen.blit(txt_surface, (box.x + 5, box.y + 5))
                label_surface = self.font.render(labels[i], True, (0, 0, 0))
                self.screen.blit(label_surface, (box.x, box.y - 40))

            self.addQuestionButton.drawWithText(self.screen)
            self.backButton.drawWithText(self.screen)
            pygame.display.flip()

            if event is not None:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.activeInput = None
                    for i, box in enumerate(self.inputBoxes):
                        if box.collidepoint(event.pos):
                            self.activeInput = i
                            break
                    if self.addQuestionButton.isClicked(event):
                        self.saveNewQuestionToFile()
                        self.newQuestion = ''
                        self.newAnswers = ['', '', '', '']
                        self.correctAnswer = ''
                    elif self.backButton.isClicked(event):
                        Screen.currentScreen = "menu"

                elif event.type == pygame.KEYDOWN and self.activeInput is not None:
                    if event.key == pygame.K_BACKSPACE:
                        if self.activeInput == 0:
                            self.newQuestion = self.newQuestion[:-1]
                        elif 1 <= self.activeInput <= 4:
                            self.newAnswers[self.activeInput - 1] = self.newAnswers[self.activeInput - 1][:-1]
                        elif self.activeInput == 5:
                            self.correctAnswer = self.correctAnswer[:-1]
                    else:
                        char = event.unicode
                        if self.activeInput == 0:
                            self.newQuestion += char
                        elif 1 <= self.activeInput <= 4:
                            self.newAnswers[self.activeInput - 1] += char
                        elif self.activeInput == 5:
                            self.correctAnswer += char

        elif Screen.currentScreen == 'choose_quiz':
            self.screen.fill("teal")
            OOP = Rect_Button(640, 300, self.buttonWidth, self.buttonHeight, 'OOP Quiz',
                                          self.font, self.fontColor, self.backgroundColor)
            custom_quiz = Rect_Button(640, 420, self.buttonWidth, self.buttonHeight, 'custom_quiz', self.font,
                                           self.fontColor, self.backgroundColor)
            for i in [OOP,custom_quiz]:
                i.drawWithText(self.screen)
                if i.isClicked(event):
                    quizName = i.text.lower().replace(" ", "_")
                    self.currentQuizFile = f"all_questions/{quizName}.txt"
                    newQuestions = RandomQuiz(self.currentQuizFile)
                    newQuestions.run()
                    self.questionScreen = QuestionScreen(newQuestions.questions)
                    self.questions = newQuestions.questions
                    Screen.currentScreen = "menu"
            pygame.display.flip()
            

        elif Screen.currentScreen == 'questions' and len(ChangeQuestion.questionHistory) != 20:
            elapsedTime = pygame.time.get_ticks() - self.startTime
            self.screen.fill("teal")
            remainingTime = max(0, (self.questionDuration - elapsedTime) // 1000)
            timerText = self.font.render(f"Czas: {remainingTime}", True, (255, 0, 0))
            self.screen.blit(timerText, (580, 0))
            self.questionScreen.drawQuestionScreen()
            pygame.display.flip()

            currentTime = pygame.time.get_ticks()

            if self.waitingForNextQuestion:
                currentTime = pygame.time.get_ticks()
                if currentTime - self.answerShownTime >= self.answerDisplayDuration:
                    self.questionScreen.changeQuestionScreen(None)
                    for i in self.questionScreen.buttons:
                        i.backgroundColor = (255, 255, 255)
                        i.drawWithText(self.screen)
                    pygame.display.flip()
                    self.startTime = pygame.time.get_ticks()
                    self.waitingForNextQuestion = False
        
            elif elapsedTime >= self.questionDuration and not self.waitingForNextQuestion:
                for j in self.questionScreen.buttons[:4]:
                    if j.text == self.questionScreen.currentQuestion.answer:
                        j.backgroundColor = (0, 255, 0)
                    else:
                        j.backgroundColor = (255, 0, 0)
                    j.drawWithText(self.screen)
                pygame.display.flip()
                self.waitingForNextQuestion = True
                self.answerShownTime = pygame.time.get_ticks()
    
            elif event is not None and event.type == pygame.MOUSEBUTTONDOWN:
                for i in self.questionScreen.buttons:
                    if i.isClicked(event):
                        if i.text == self.questionScreen.currentQuestion.answer:
                            self.questionScreen.correctQuestions += 1
                            print(self.questionScreen.correctQuestions)
                        if i.text != "50/50" and i.text != "Phone":
                            for j in self.questionScreen.buttons[:4]:
                                if j.text == self.questionScreen.currentQuestion.answer:
                                    
                                    j.backgroundColor = (0, 255, 0)
                                else:
                                    j.backgroundColor = (255, 0, 0)
                                j.drawWithText(self.screen)
                            pygame.display.flip()
                            self.waitingForNextQuestion = True
                            self.answerShownTime = currentTime

                        elif i.text == "50/50":
                            self.questionScreen.applyLifeline("50/50")
                        elif i.text == "Phone":
                            self.questionScreen.applyLifeline("call")
                        break

           
            
        else:
            self.screen.fill("teal")
            text = self.font.render(f"Uzyskano {self.questionScreen.correctQuestions}/20", True, (255, 255, 255))
            self.screen.blit(text, (540, 100))
            RetryQuizButton = Rect_Button(640, 300, self.buttonWidth, self.buttonHeight, 'Spróbuj ponownie',
                                                     self.font, self.fontColor, self.backgroundColor)
            ChangeQuizButton = Rect_Button(640, 420, self.buttonWidth, self.buttonHeight, 'Zmień Quiz', self.font,
                                           self.fontColor, self.backgroundColor)
            MenuButton = Rect_Button(640, 540, self.buttonWidth, self.buttonHeight, 'Menu',
                                                self.font, self.fontColor, self.backgroundColor)

            RetryQuizButton.drawWithText(self.screen)
            ChangeQuizButton.drawWithText(self.screen)
            MenuButton.drawWithText(self.screen)

            if event is not None and event.type == pygame.MOUSEBUTTONDOWN:

                if ChangeQuizButton.isClicked(event):
                    Screen.currentScreen = "choose_quiz"
                    ChangeQuestion.questionHistory = []
                    QuestionScreen.correctQuestions = 0

                if RetryQuizButton.isClicked(event):
                    ChangeQuestion.questionHistory = []
                    QuestionScreen.correctQuestions = 0

                    newQuestions = RandomQuiz(self.currentQuizFile)
                    newQuestions.run()
                    self.questions = newQuestions.questions
                    self.questionScreen = QuestionScreen(self.questions)
                    Screen.currentScreen = "questions"
                    self.startTime = pygame.time.get_ticks()

                if MenuButton.isClicked(event):
                    ChangeQuestion.questionHistory = []
                    QuestionScreen.correctQuestions = 0

                    newQuestions = RandomQuiz(self.currentQuizFile)
                    newQuestions.run()
                    self.questions = newQuestions.questions
                    self.questionScreen = QuestionScreen(self.questions)
                    Screen.currentScreen = "menu"




            pygame.display.flip()

    def saveNewQuestionToFile(self):
        try:
            if len(self.newQuestion.strip()) == 0 or len(self.correctAnswer.strip()) == 0:
                raise ErrorDodawaniaPytan("Pytanie i poprawna odpowiedź nie mogą być puste.")

            if any(ans.strip() == '' for ans in self.newAnswers):
                raise ErrorDodawaniaPytan("Wszystkie odpowiedzi muszą być wypełnione.")

            if self.correctAnswer.strip() not in [a.strip() for a in self.newAnswers]:
                raise ErrorDodawaniaPytan("Poprawna odpowiedź musi znajdować się wśród odpowiedzi.")

            with open('all_questions/custom_quiz.txt', 'a', encoding='utf-8') as f:
                line = f"\n{self.newQuestion.strip()}|{self.newAnswers[0].strip()}|{self.newAnswers[1].strip()}|{self.newAnswers[2].strip()}|{self.newAnswers[3].strip()}|{self.correctAnswer.strip()}"
                f.write(line)

            print("Dodano poprawne pytanie!")

            self.newQuestion = ''
            self.newAnswers = ['', '', '', '']
            self.correctAnswer = ''

        except ErrorDodawaniaPytan as e:
            print(f"Błąd dodawania pytania: {e}")
