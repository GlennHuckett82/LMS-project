"""Reset or create a sample lesson record for quick manual testing."""

from lessons.models import Lesson
from courses.models import Course

# Ensure course with id=2 exists
course, _ = Course.objects.get_or_create(id=2, defaults={'title': 'Intro to Python'})

# Create or update lesson with id=4 for course 2
lesson, _ = Lesson.objects.update_or_create(
    id=4,
    defaults={
        'title': 'Python module one',
        'course': course,
        'order': 1,
        'content': '<h1>Welcome to Python Module One!</h1>'
    }
)
print(f"Lesson ID: {lesson.id}, Title: {lesson.title}, Course ID: {lesson.course.id}, Course Title: {lesson.course.title}")
