import json

class Question:
    def __init__(self, q_id, text, answer, q_type="quiz", enabled=True, times_shown=0, times_correct=0):
        self.q_id = q_id
        self.text = text
        self.answer = answer
        self.q_type = q_type
        self.enabled = enabled
        self.times_shown = times_shown
        self.times_correct = times_correct

    def check_answer(self, user_answer):
        self.times_shown += 1
        if self.q_type == "quiz":
            is_correct = user_answer.strip().upper() == self.answer.strip().upper()
        else:
            is_correct = user_answer.strip().lower() == self.answer.strip().lower()
            
        if is_correct:
            self.times_correct += 1
        return is_correct

    def get_correct_percentage(self):
        if self.times_shown == 0:
            return 0
        return round((self.times_correct / self.times_shown) * 100, 2)

    def to_dict(self):
        return {
            "q_id": self.q_id,
            "text": self.text,
            "answer": self.answer,
            "q_type": self.q_type,
            "enabled": self.enabled,
            "times_shown": self.times_shown,
            "times_correct": self.times_correct
        }

    @classmethod
    def from_dict(cls, data):
        q = cls(data["q_id"], data["text"], data["answer"], data["q_type"], data["enabled"])
        q.times_shown = data["times_shown"]
        q.times_correct = data["times_correct"]
        return q


# Freeform test
# if __name__ == "__main__":
#     print("Testing Question class! ")
#     q = Question(99, "Is ice cream tasty?", "yes", q_type="freeform")
#     print("Question:", q.text)
#     user_answer = input("Your answer: ")
#     print("Correct!" if q.check_answer(user_answer) else "Oops, wrong!")
#     print("Stats: Shown", q.times_shown, "times, Correct:", q.times_correct)



# Quiz questions test
# if __name__ == "__main__":
#     print("\n Testing Multiple-Choice Question! ")
    
#     # Create a quiz question with choices
#     q = Question(
#         q_id=101,
#         text="What is the capital of France?",
#         answer="B",  # Correct choice is "B"
#         q_type="quiz",
#         choices=["A) London", "B) Paris", "C) Rome", "D) Berlin"]
#     )

#     # Print the question and choices
#     print("Q:", q.text)
#     for choice in q.choices:
#         print(choice)

#     # Simulate user answering "B" (correct) and "C" (wrong)
#     print("\nTesting answer 'B':", q.check_answer("B"))  # Should return True
#     print("Testing answer 'C':", q.check_answer("C"))  # Should return False

#     # Show stats
#     print("\nStats: Shown", q.times_shown, "times, Correct:", q.times_correct)
#     print("Win Rate:", q.get_correct_percentage(), "%")