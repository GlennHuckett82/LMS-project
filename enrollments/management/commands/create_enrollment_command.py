
"""Utility management command to enroll the first student into the first course."""

from django.core.management.base import BaseCommand
from accounts.models import User
from courses.models import Course
from enrollments.models import Enrollment

class Command(BaseCommand):
    help = "Enrolls the first available student into the first available course."

    def handle(self, *args, **kwargs):
        try:
            # Get the first student
            student = User.objects.filter(role='student').first()
            if not student:
                self.stdout.write(self.style.ERROR("No students found. Please run populate_db.py first."))
                return

            # Get the first course
            course = Course.objects.first()
            if not course:
                self.stdout.write(self.style.ERROR("No courses found. Please run 'python manage.py seed' first."))
                return

            # Check if enrollment already exists
            if Enrollment.objects.filter(student=student, course=course).exists():
                self.stdout.write(self.style.SUCCESS(f"Student '{student.username}' is already enrolled in course '{course.title}'."))
                return

            # Create enrollment
            Enrollment.objects.create(student=student, course=course)
            self.stdout.write(self.style.SUCCESS(f"Successfully enrolled student '{student.username}' in course '{course.title}'."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
