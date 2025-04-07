import os
import json
from question import Question

DATA_FILE = "data/questions.json"

class QuestionDatabase:
    def __init__(self):
        self.questions = []
        self.load()

    def load(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                    self.questions = [Question.from_dict(q) for q in data]
        except (json.JSONDecodeError, IOError):
            self.questions = []

    def save(self):
        try:
            with open(DATA_FILE, "w") as f:
                json.dump([q.to_dict() for q in self.questions], f, indent=4)
        except IOError:
            print("Error: Could not save questions.")

    def add_question(self, question):
        self.questions.append(question)
        self.save()

    def get_question_by_id(self, q_id):
        return next((q for q in self.questions if q.q_id == q_id), None)

    def get_enabled_questions(self):
        return [q for q in self.questions if q.enabled]

    def get_all_questions(self):
        return self.questions.copy()
