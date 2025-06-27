class Quiz:
    def run(self):
        self.load_questions()
        self.get_questions()

    def load_questions(self):
        raise NotImplementedError

    def get_questions(self):
        raise NotImplementedError


class RandomQuiz(Quiz):
    def __init__(self):
        self.questions = []

    def load_questions(self):
        with open('all_questions/questions0.txt', 'r', encoding='utf-8') as data:
            questions = data.read()
            questions = questions.split('\n')
            for question in questions:
                self.questions.append(question.split('|'))

    def get_questions(self):
        return self.questions