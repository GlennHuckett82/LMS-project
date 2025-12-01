
import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms_backend.settings")
django.setup()

from accounts.models import User
from courses.models import Course
from enrollments.models import Enrollment

def create_enrollment():
    """
    Enrolls the first available student into the first available course.
    """
    try:
        # Get the first student
        student = User.objects.filter(role='student').first()
        if not student:
            print("No students found. Please run populate_db.py first.")
            return

        # Get the first course
        course = Course.objects.first()
        if not course:
            print("No courses found. Please run 'python manage.py seed' first.")
            return

        # Check if enrollment already exists
        if Enrollment.objects.filter(student=student, course=course).exists():
            print(f"Student '{student.username}' is already enrolled in course '{course.title}'.")
            return

        # Create enrollment
        Enrollment.objects.create(student=student, course=course)
        print(f"Successfully enrolled student '{student.username}' in course '{course.title}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_enrollment()
