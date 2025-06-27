from abc import ABC, abstractmethod

from classes.question import QuestionScreen, ChangeQuestion
from classes.setup import Setup
from components.button import Rect_Button
from components.questionHeader import QuestionHeader
import pygame
from random import choice

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

        self.startTime = pygame.time.get_ticks()
        self.questionDuration = 31000

    def handle(self, event):
        elapsedTime = pygame.time.get_ticks() - self.startTime

        if Screen.currentScreen == "menu":
            self.screen.fill("teal")
            self.startButton.drawWithText(self.screen)
            self.goToAddQuestionButton.drawWithText(self.screen)
            pygame.display.flip()

            if event is not None and event.type == pygame.MOUSEBUTTONDOWN:
                if self.startButton.isClicked(event):
                    Screen.currentScreen = "questions"
                    self.startTime = pygame.time.get_ticks()
                elif self.goToAddQuestionButton.isClicked(event):
                    Screen.currentScreen = "add_question"

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

        elif Screen.currentScreen == 'questions' and len(ChangeQuestion.questionHistory) != 20:
            remainingTime = max(0, (self.questionDuration - elapsedTime) // 1000)
            timerText = self.font.render(f"Czas: {remainingTime}", True, (255, 0, 0))
            correct = self.font.render(str(QuestionScreen.correctQuestions), 1, self.fontColor, None)

            self.screen.fill("teal")
            self.screen.blit(timerText, (500, 0))
            self.screen.blit(correct, (0, 0), None)
            self.questionScreen.drawQuestionScreen()
            pygame.display.flip()

            if event is not None and event.type == pygame.MOUSEBUTTONDOWN:
                for i in self.questionScreen.buttons:
                    if i.isClicked(event):
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

    def saveNewQuestionToFile(self):
        try:
            if len(self.newQuestion.strip()) == 0 or len(self.correctAnswer.strip()) == 0:
                raise ErrorDodawaniaPytan("Pytanie i poprawna odpowiedź nie mogą być puste.")

            if any(ans.strip() == '' for ans in self.newAnswers):
                raise ErrorDodawaniaPytan("Wszystkie odpowiedzi muszą być wypełnione.")

            if self.correctAnswer.strip() not in [a.strip() for a in self.newAnswers]:
                raise ErrorDodawaniaPytan("Poprawna odpowiedź musi znajdować się wśród odpowiedzi.")

            with open('all_questions/questions0.txt', 'a', encoding='utf-8') as f:
                line = f"\n{self.newQuestion.strip()}|{self.newAnswers[0].strip()}|{self.newAnswers[1].strip()}|{self.newAnswers[2].strip()}|{self.newAnswers[3].strip()}|{self.correctAnswer.strip()}"
                f.write(line)

            print("Dodano poprawne pytanie!")

            # Reset pól po dodaniu pytania
            self.newQuestion = ''
            self.newAnswers = ['', '', '', '']
            self.correctAnswer = ''

        except ErrorDodawaniaPytan as e:
            print(f"Błąd dodawania pytania: {e}")
