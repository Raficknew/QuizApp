from abc import ABC, abstractmethod

from classes.lifebuoys import LifelineContext, CallAFriend, FiftyFifty
from classes.setup import Setup
from components.button import Rect_Button
from components.questionHeader import QuestionHeader
from random import choice

class Command(ABC):

    @abstractmethod
    def execute(self):
        pass


class Question:

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

    @property
    def question(self):
        return (self._questionTitle, self._answers, self._answer)

    @question.setter
    def question(self, value):
        newTitle, newAnswers, newAnswer = value
        self._questionTitle = newTitle
        self._answers = newAnswers
        self._answer = newAnswer

    def __str__(self):
        return f"{self.questionTitle}, {self.answers}, {self.answer}"


class ChangeQuestion(Command):
    questionHistory = []

    def __init__(self, question, newQuestionTitle, newAnswer, newAnswers):
        self.question = question
        self.newQuestionTitle = newQuestionTitle
        self.newAnswer = newAnswer
        self.newAnswers = newAnswers

    def execute(self):
        ChangeQuestion.questionHistory.append(
            (self.question.questionTitle, self.question.answers, self.question.answer)
        )

        self.question.question = (self.newQuestionTitle, self.newAnswers, self.newAnswer)

    def __str__(self):
        return f"{ChangeQuestion.questionHistory}"


class QuestionScreen(Setup):
    correctQuestions = 0

    def __init__(self, questions):

        super().__init__()
        self.questions = questions
        self.firstRandomQuestion = choice(questions)
        self.currentQuestion = Question(self.firstRandomQuestion[0], self.firstRandomQuestion[1:-1],
                                        self.firstRandomQuestion[-1])
        self.questions.remove(self.firstRandomQuestion)
        self.b1 = Rect_Button(640, 250, self.buttonWidth, self.buttonHeight, self.currentQuestion.answers[0], self.font,
                              self.fontColor, self.backgroundColor)
        self.b2 = Rect_Button(640, 370, self.buttonWidth, self.buttonHeight, self.currentQuestion.answers[1], self.font,
                              self.fontColor, self.backgroundColor)
        self.b3 = Rect_Button(640, 490, self.buttonWidth, self.buttonHeight, self.currentQuestion.answers[2], self.font,
                              self.fontColor, self.backgroundColor)
        self.b4 = Rect_Button(640, 610, self.buttonWidth, self.buttonHeight, self.currentQuestion.answers[3], self.font,
                              self.fontColor, self.backgroundColor)
        self.b50 =  Rect_Button(60, 700, 100, self.buttonHeight, "50/50", self.font,
                              self.fontColor, self.backgroundColor)
        self.bPhone = Rect_Button(170, 700, 100, self.buttonHeight, "Phone", self.font,
                               self.fontColor, self.backgroundColor)
        self.buttons = [self.b1, self.b2, self.b3, self.b4, self.b50, self.bPhone]
        self.header = QuestionHeader(640, 100, self.buttonWidth, self.buttonHeight, self.currentQuestion.questionTitle,
                                     self.font, self.fontColor, self.backgroundColor)
        self.objects = self.buttons + [self.header]

        self.used_lifelines = {"50/50": False, "call": False}
        self.current_lifeline_result = None

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
        ChangeQuestion(self.currentQuestion, newQuestion[0], newQuestion[-1], newQuestion[1:-1]).execute()
        self.current_lifeline_result = None
        self.header.updateText(self.currentQuestion.questionTitle)
        self.used_lifelines = {"50/50": self.used_lifelines["50/50"], "call": self.used_lifelines["call"]}

    def applyLifeline(self, name):
        if name == "50/50" and not self.used_lifelines["50/50"]:
            lifeline = LifelineContext(FiftyFifty())
            reduced_answers = lifeline.execute(self.currentQuestion)
            self.current_lifeline_result = reduced_answers
            self.used_lifelines["50/50"] = True

            for button in self.buttons:
                if button.text not in reduced_answers and button.text not in ["50/50", "Phone"]:
                    button.updateText("")

            if self.b50 in self.buttons:
                self.buttons.remove(self.b50)
            if self.b50 in self.objects:
                self.objects.remove(self.b50)

        elif name == "call" and not self.used_lifelines["call"]:
            lifeline = LifelineContext(CallAFriend())
            suggestion = lifeline.execute(self.currentQuestion)
            print(f"Przyjaciel sugeruje: {suggestion}")
            self.used_lifelines["call"] = True


            if self.bPhone in self.buttons:
                self.buttons.remove(self.bPhone)
            if self.bPhone in self.objects:
                self.objects.remove(self.bPhone)

    def changeQuestionScreen(self, event):
        if event is None:
            self.newQuestion()
            for button, j in zip(self.buttons[:4], range(4)):
                button.updateText(self.currentQuestion.answers[j])
            return

        for button in self.objects:
            if button.isClicked(event):
                if "?" in button.text:
                    return
                if button.text == "50/50":
                    self.applyLifeline("50/50")
                    return
                elif button.text == "Phone":
                    self.applyLifeline("call")
                    return
                elif button.text == self.currentQuestion.answer:
                    QuestionScreen.correctQuestions += 1
                self.newQuestion()
                for button, j in zip(self.buttons[:4], range(4)):
                    button.updateText(self.currentQuestion.answers[j])
                break


