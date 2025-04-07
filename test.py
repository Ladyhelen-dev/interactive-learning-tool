import unittest
from question import Question
from database import QuestionDatabase
from main import weighted_choice

class TestQuestion(unittest.TestCase):
    def test_check_answer_correct(self):
        q = Question(1, "What is 2+2?", "4")
        self.assertTrue(q.check_answer("4"))

    def test_check_answer_wrong(self):
        q = Question(2, "Capital of France?", "Paris")
        self.assertFalse(q.check_answer("London"))

    def test_correct_percentage(self):
        q = Question(3, "Test", "A")
        q.check_answer("A")  # Correct
        q.check_answer("B")  # Wrong
        self.assertEqual(q.get_correct_percentage(), 50.0)

    def test_database_save_load(self):
        db = QuestionDatabase()
        q = Question(99, "Database test?", "Yes")
        db.add_question(q)
        
        new_db = QuestionDatabase()
        loaded_q = new_db.get_question_by_id(99)
        self.assertEqual(loaded_q.text, "Database test?")

    def test_weighted_choice(self):
        q1 = Question(1, "Easy", "A")
        q2 = Question(2, "Hard", "B")
        q1.times_shown = 10
        q1.times_correct = 9  # 90% correct
        q2.times_shown = 10
        q2.times_correct = 2  # 20% correct
        
        questions = [q1, q2]
        result = weighted_choice(questions)
        self.assertEqual(result.q_id, 2)  # Harder question should be picked

if __name__ == "__main__":
    unittest.main()