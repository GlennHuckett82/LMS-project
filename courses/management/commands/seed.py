
from django.core.management.base import BaseCommand
from courses.models import Course
from accounts.models import User   # your custom user model

# This Django management command quickly fills the database with fake teachers and courses for testing.
# It deletes any existing teachers/courses, then creates new ones so you always start with a clean slate.
class Command(BaseCommand):
    help = "Seed the database with fake teachers and courses"

    def handle(self, *args, **kwargs):
        # List of teacher names and course titles to create.
        teachers = ["Alice", "Bob", "Charlie", "Dana", "Ethan"]
        courses = [
            "Intro to Python",
            "Frontend with React",
            "Data Structures",
            "Databases",
            "DevOps Fundamentals"
        ]

        # Remove all existing courses and teacher users so we don't get duplicates.
        Course.objects.all().delete()
        User.objects.filter(role="teacher").delete()

        # Create each teacher and their course.
        for name, course_title in zip(teachers, courses):
            # Make a new teacher user with a simple default password.
            teacher = User.objects.create_user(
                username=name.lower(),
                password="password123",   # simple default password
                role="teacher",
                first_name=name
            )

            # Make a new course and link it to the teacher we just created.
            Course.objects.create(
                title=course_title,
                description=f"{course_title} taught by {name}.",
                teacher=teacher
            )

        # Print a success message so you know the command finished.
        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))