class Quiz:
    def run(self):
        self.load_questions()
        self.get_questions()

    def load_questions(self):
        raise NotImplementedError

    def get_questions(self):
        raise NotImplementedError


class RandomQuiz(Quiz):
    
    def __init__(self,textFile):
        self.questions = []
        self.textFile = textFile

    def load_questions(self):
        
        with open(self.textFile, 'r', encoding='utf-8') as data:
            questions = data.read().split('\n')
            for question in questions:
                self.questions.append(question.split('|'))

    def get_questions(self):
        return self.questions