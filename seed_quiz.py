"""Create a sample quiz for the first lesson to aid demos."""

import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms_backend.settings")
django.setup()

from lessons.models import Lesson
from quizzes.models import Quiz, Question, Choice

def seed_quiz():
    """
    Creates a sample quiz for the first lesson if it doesn't already exist.
    """
    try:
        # 1. Get the first lesson
        first_lesson = Lesson.objects.order_by('id').first()
        if not first_lesson:
            print("No lessons found. Please create some lessons first (e.g., by running 'seed_lessons.py').")
            return

        # 2. Check if a quiz already exists for this lesson
        if Quiz.objects.filter(lesson=first_lesson).exists():
            print(f"A quiz for the lesson '{first_lesson.title}' already exists. Skipping.")
            return

        # 3. Create the Quiz
        quiz = Quiz.objects.create(
            lesson=first_lesson,
            title=f"Quiz for: {first_lesson.title}"
        )
        print(f"Successfully created quiz for lesson: '{first_lesson.title}'")

        # 4. Define the questions and choices
        quiz_data = [
            {
                "text": "What does HTML stand for?",
                "explanation": "HTML is the standard markup language for creating web pages and web applications.",
                "choices": [
                    {"text": "Hyper Trainer Marking Language", "is_correct": False},
                    {"text": "Hyper Text Markup Language", "is_correct": True},
                    {"text": "High-Level Textual Markup Language", "is_correct": False},
                    {"text": "Home Tool Markup Language", "is_correct": False},
                ]
            },
            {
                "text": "Which of the following is a CSS preprocessor?",
                "explanation": "Sass (Syntactically Awesome Style Sheets) is a preprocessor scripting language that is interpreted or compiled into CSS.",
                "choices": [
                    {"text": "Sass", "is_correct": True},
                    {"text": "React", "is_correct": False},
                    {"text": "TypeScript", "is_correct": False},
                    {"text": "Django", "is_correct": False},
                ]
            },
            {
                "text": "What is the purpose of a 'foreign key' in a database?",
                "explanation": "A foreign key is a key used to link two tables together. It is a field (or collection of fields) in one table that refers to the PRIMARY KEY in another table.",
                "choices": [
                    {"text": "To uniquely identify a record in a table.", "is_correct": False},
                    {"text": "To link two tables together.", "is_correct": True},
                    {"text": "To speed up data retrieval.", "is_correct": False},
                    {"text": "To store large text data.", "is_correct": False},
                ]
            }
        ]

        # 5. Create Questions and Choices
        for question_data in quiz_data:
            question = Question.objects.create(
                quiz=quiz,
                text=question_data["text"],
                explanation=question_data["explanation"]
            )
            print(f"  - Created question: '{question.text[:30]}...'")
            for choice_data in question_data["choices"]:
                Choice.objects.create(
                    question=question,
                    text=choice_data["text"],
                    is_correct=choice_data["is_correct"]
                )
        
        print("\nSample quiz data has been successfully created.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    seed_quiz()
