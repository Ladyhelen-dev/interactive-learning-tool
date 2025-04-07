from question import Question
from database import QuestionDatabase
import random
import datetime

db = QuestionDatabase()

def get_next_question_id():
    if not db.questions:
        return 1
    return max(q.q_id for q in db.questions) + 1

def add_question():
    q_type = input("Enter question type (quiz or freeform): ").strip().lower()
    if q_type not in ["quiz", "freeform"]:
        print("Invalid type.")
        return

    text = input("Enter question text: ").strip()
    answer = input("Enter the correct answer: ").strip()

    q_id = get_next_question_id()
    new_question = Question(q_id, text, answer, q_type)
    db.add_question(new_question)
    db.save_questions()
    print(f"Question added with ID {q_id}.")

def show_statistics():
    for q in db.get_all_questions():
        print(f"ID: {q.q_id}, Active: {q.enabled}, Question: {q.text}")
        print(f"  Times Shown: {q.times_shown}, Correct %: {q.get_correct_percentage()}%")

def toggle_question():
    if not db.questions:
        print("No questions to toggle.")
        return
        
    while True:
        try:
            q_id = int(input("Enter question ID: "))
            break
        except ValueError:
            print("Please enter a number.")

    question = db.get_question_by_id(q_id)
    if not question:
        print("Question not found.")
        return

    print(f"\nCurrent Question: {question.text}")
    action = "enable" if not question.enabled else "disable"
    confirm = input(f"{action.capitalize()} this question? (y/n): ").lower()
    
    if confirm == "y":
        question.enabled = not question.enabled
        db.save_questions()
        print(f"Question {action}d.")
    else:
        print("Action cancelled.")

def weighted_choice(questions):
    weights = []
    for q in questions:
        if q.times_shown == 0:
            weights.append(1.0)
        else:
            weight = 1.0 - (q.times_correct / q.times_shown)
            weights.append(weight)
    return random.choices(questions, weights=weights, k=1)[0]

def practice_mode():
    questions = db.get_enabled_questions()
    if len(questions) < 5:
        print("You need at least 5 questions to practice.")
        return

    print("\n=== Practice Mode ===")
    print("Type 'quit' to stop):")
    
    try:
        while True:
            q = weighted_choice(questions)
            print(f"Q: {q.text}")
            
            user_answer = input("Your answer: ").strip()
            if user_answer.lower() == "quit":
                break

            if q.check_answer(user_answer):
                print("Correct!")
            else:
                print(f"Wrong! Correct answer: {q.answer}")
                
            db.save_questions()
    except KeyboardInterrupt:
        pass
    print("Exiting practice mode.")

def test_mode():
    questions = db.get_enabled_questions()
    if len(questions) < 5:
        print("You need at least 5 questions to enter test mode.")
        return
    
    print("\n=== Test Mode ===")
    while True:
        try:
            num = int(input(f"Number of questions (1-{len(questions)}): "))
            if 1 <= num <= len(questions):
                break
            print(f"Please enter 1-{len(questions)}")
        except ValueError:
            print("Please enter a number.")

    test_qs = random.sample(questions, num)
    correct_count = 0
    
    for q in test_qs:
        print(f"Q: {q.text}")
        user_answer = input("Your answer: ").strip()
        if q.check_answer(user_answer):
            print("Correct!")
            correct_count += 1
        else:
            print(f"Wrong! Correct answer: {q.answer}")
            
    score = round((correct_count / num) * 100, 2)
    print(f"Test finished. Score: {score}%")

    with open("data/results.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - Score: {score}%\n")
    db.save_questions()

def main():
    while True:
        print("\n=== Interactive Learning Tool ===")
        print("1. Add Question")
        print("2. View Statistics")
        print("3. Enable/Disable Question")
        print("4. Practice Mode")
        print("5. Test Mode")
        print("0. Exit")

        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            add_question()
        elif choice == "2":
            show_statistics()
        elif choice == "3":
            toggle_question()
        elif choice == "4":
            practice_mode()
        elif choice == "5":
            test_mode()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 0-5.")

if __name__ == "__main__":
    main()