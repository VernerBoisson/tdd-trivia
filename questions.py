from utils import Utils

class Question:
    def __init__(self, question):
        self.question = question
    
class Questions:
    def __init__(self, category_name):
        self.category_name = category_name
        self.questions = []
    
    def add_question(self, question):
        self.questions.append(question)

    def generate_questions(self, number_of_questions):
        [self.add_question(\
            Question(Utils.template_log('add_question',\
                question_category=self.category_name,\
                question_number=self.questions.__len__())))\
            for _ in range(number_of_questions)]

    def get_last_question(self):
        if self.questions.__len__() > 0:
            return self.questions[self.questions.__len__() - 1]

    def drop_last_question(self):
        if self.questions.__len__() > 0:
            self.questions.pop()
    
    def is_empty(self):
        return self.questions.__len__() == 0

    def __len__(self):
        return len(self.questions)
