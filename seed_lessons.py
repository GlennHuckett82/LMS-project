from lessons.models import Lesson
from courses.models import Course

# This script seeds the database with a correct lesson for testing.
# Run with: python manage.py shell < seed_lessons.py

def run():
    # Find the course you want to add the lesson to
    course = Course.objects.filter(title__icontains="Intro to Python").first()
    if not course:
        print("Course 'Intro to Python' not found.")
        return

    # Create or update the lesson
    lesson, created = Lesson.objects.update_or_create(
        course=course,
        order=1,
        defaults={
            "title": "Python module one",
            "content": "<h3>Lesson: Working with Variables</h3><p>In Python, we use variables to store information. In the code below, we've stored the name 'Alice' in a variable called <code>name</code>.</p><p><strong>Your Task:</strong> Complete the code to make it print the greeting 'Hello, Alice'. Drag the correct code block from the right and drop it into the empty space.</p><pre><code>name = 'Alice'\n# Your code goes here!</code></pre>",
        }
    )
    if created:
        print("Lesson 'Python module one' created.")
    else:
        print("Lesson 'Python module one' updated.")

run()
