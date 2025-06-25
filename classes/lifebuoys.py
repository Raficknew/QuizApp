from abc import ABC, abstractmethod
import random


class Lifebuoys(ABC):
    @abstractmethod
    def use(self,question):
        pass

class FiftyFifty:
    def use(self, question):
        correct = question.answer
        other = [a for a in question.answers if a != correct]
        chosen = random.choice(other)
        return [correct, chosen]

class CallAFriend(Lifebuoys):
    def use(self, question):
        if random.random() < 0.90:
            return question.answer
        else:
            wrong_answers = [a for a in question.answers if a != question.answer]
            return random.choice(wrong_answers)

class LifelineContext:
    def __init__(self, strategy: Lifebuoys):
        self.strategy = strategy

    def execute(self, question):
        return self.strategy.use(question)