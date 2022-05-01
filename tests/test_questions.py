import unittest
from questions import Questions, Question


class TestQuestion(unittest.TestCase):
    def test_question_init(self):
        question = Question('question')
        self.assertEqual(question.question, 'question')

class TestQuestions(unittest.TestCase):
    def test_questions_init(self):
        questions = Questions('category')
        self.assertEqual(questions.category_name, 'category')
        self.assertEqual(questions.questions, [])

    def test_questions_add_question(self):
        questions = Questions('category')
        questions.add_question(Question('question'))
        self.assertEqual(len(questions.questions), 1)
        self.assertIsInstance(questions.questions[0], Question)

    def test_generate_questions(self):
        questions = Questions('category')
        questions.generate_questions(5)
        self.assertEqual(len(questions.questions), 5)
        self.assertIsInstance(questions.questions[0], Question)
        
    def test_get_last_question(self):
        questions = Questions('category')
        questions.add_question(Question('question 1'))
        questions.add_question(Question('question 2'))
        self.assertIsInstance(questions.get_last_question(), Question)
        self.assertEqual(questions.get_last_question(), questions.questions[-1])
        self.assertEqual(questions.get_last_question().question, 'question 2')

    def drop_last_question(self):
        questions = Questions('category')
        questions.add_question(Question('question 1'))
        questions.add_question(Question('question 2'))
        questions.drop_last_question()
        self.assertEqual(len(questions.questions), 1)
        self.assertIsInstance(questions.questions[0], Question)
        self.assertEqual(questions.questions[0].question, 'question 1')

    def test_is_empty(self):
        questions = Questions('category')
        self.assertTrue(questions.is_empty())
        questions.add_question(Question('question'))
        self.assertFalse(questions.is_empty())
    
    def test_len(self):
        questions = Questions('category')
        self.assertEqual(len(questions), 0)
        questions.add_question(Question('question'))
        self.assertEqual(len(questions), 1)
        questions.add_question(Question('question'))
        self.assertEqual(len(questions), 2)



if __name__ == '__main__':
    unittest.main()