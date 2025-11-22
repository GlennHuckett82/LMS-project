from django.core.management.base import BaseCommand
from courses.models import Course
from accounts.models import User   # your custom user model

class Command(BaseCommand):
    help = "Seed the database with fake teachers and courses"

    def handle(self, *args, **kwargs):
        teachers = ["Alice", "Bob", "Charlie", "Dana", "Ethan"]
        courses = [
            "Intro to Python",
            "Frontend with React",
            "Data Structures",
            "Databases",
            "DevOps Fundamentals"
        ]

        # Clear existing data
        Course.objects.all().delete()
        User.objects.filter(role="teacher").delete()

        for name, course_title in zip(teachers, courses):
            # Create a teacher user
            teacher = User.objects.create_user(
                username=name.lower(),
                password="password123",   # simple default password
                role="teacher",
                first_name=name
            )

            # Create a course linked to that teacher
            Course.objects.create(
                title=course_title,
                description=f"{course_title} taught by {name}.",
                teacher=teacher
            )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))