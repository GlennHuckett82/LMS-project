# Run the script with: python manage.py shell < print_lesson_course_ids.py
from lessons.models import Lesson
for lesson in Lesson.objects.all():
    print(f"Lesson ID: {lesson.id}, Title: {lesson.title}, Course ID: {lesson.course.id}, Course Title: {lesson.course.title}")
