from django.core.management.base import BaseCommand
from django.core.management import call_command

from courses.models import Course
from lessons.models import Lesson
from quizzes.models import Quiz, Question, Choice


class Command(BaseCommand):
    help = "Initialise demo data: demo roles and seeded teachers, courses, lessons, and one demo quiz."

    def handle(self, *args, **options):
        self.stdout.write("Running set_demo_roles...")
        call_command("set_demo_roles")

        self.stdout.write("Running courses.seed...")
        call_command("seed")

        # After the generic seed, ensure a rich Intro to Python lesson plus a linked quiz
        self._ensure_demo_lesson_and_quiz()

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data initialised (demo users, teachers, courses, lessons, quiz)."
            )
        )

    def _ensure_demo_lesson_and_quiz(self) -> None:
        """Create/update a concrete Intro to Python lesson and attach a sample quiz.

        This mirrors the behaviour you had locally via seed_lessons.py and seed_quiz.py
        so that the deployed app also shows real lesson content and a quiz + score page.
        """

        course = Course.objects.filter(title__icontains="Intro to Python").first()
        if not course:
            self.stdout.write("Intro to Python course not found; skipping demo lesson/quiz.")
            return

        # Ensure there is a well-defined first lesson with rich HTML content
        lesson_content = (
            "<h3>Lesson: Working with Variables</h3>"
            "<p>In Python, we use variables to store information. In the code below, we've "
            "stored the name 'Alice' in a variable called <code>name</code>.</p>"
            "<p><strong>Your Task:</strong> Complete the code to make it print the greeting "
            "'Hello, Alice'. Drag the correct code block from the right and drop it into the "
            "empty space.</p>"
            "<pre><code>name = 'Alice'\n# Your code goes here!</code></pre>"
        )

        lesson, created = Lesson.objects.update_or_create(
            course=course,
            order=1,
            defaults={
                "title": "Python module one",
                "content": lesson_content,
            },
        )
        if created:
            self.stdout.write("Created demo lesson 'Python module one'.")
        else:
            self.stdout.write("Updated demo lesson 'Python module one'.")

        # Attach a sample quiz to the lesson if one does not already exist
        if Quiz.objects.filter(lesson=lesson).exists():
            self.stdout.write("Quiz already exists for demo lesson; leaving it unchanged.")
            return

        quiz = Quiz.objects.create(lesson=lesson, title=f"Quiz for: {lesson.title}")
        self.stdout.write(f"Created quiz for demo lesson '{lesson.title}'.")

        quiz_data = [
            {
                "text": "What does HTML stand for?",
                "explanation": (
                    "HTML is the standard markup language for creating web pages and web "
                    "applications."
                ),
                "choices": [
                    {"text": "Hyper Trainer Marking Language", "is_correct": False},
                    {"text": "Hyper Text Markup Language", "is_correct": True},
                    {"text": "High-Level Textual Markup Language", "is_correct": False},
                    {"text": "Home Tool Markup Language", "is_correct": False},
                ],
            },
            {
                "text": "Which of the following is a CSS preprocessor?",
                "explanation": (
                    "Sass (Syntactically Awesome Style Sheets) is a preprocessor scripting "
                    "language that is interpreted or compiled into CSS."
                ),
                "choices": [
                    {"text": "Sass", "is_correct": True},
                    {"text": "React", "is_correct": False},
                    {"text": "TypeScript", "is_correct": False},
                    {"text": "Django", "is_correct": False},
                ],
            },
            {
                "text": "What is the purpose of a 'foreign key' in a database?",
                "explanation": (
                    "A foreign key is a key used to link two tables together. It is a field "
                    "(or collection of fields) in one table that refers to the PRIMARY KEY in "
                    "another table."
                ),
                "choices": [
                    {
                        "text": "To uniquely identify a record in a table.",
                        "is_correct": False,
                    },
                    {"text": "To link two tables together.", "is_correct": True},
                    {"text": "To speed up data retrieval.", "is_correct": False},
                    {"text": "To store large text data.", "is_correct": False},
                ],
            },
        ]

        for question_data in quiz_data:
            question = Question.objects.create(
                quiz=quiz,
                text=question_data["text"],
                explanation=question_data["explanation"],
            )
            for choice_data in question_data["choices"]:
                Choice.objects.create(
                    question=question,
                    text=choice_data["text"],
                    is_correct=choice_data["is_correct"],
                )

        self.stdout.write("Sample quiz questions and choices created for demo lesson.")
