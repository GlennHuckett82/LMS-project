"""Seed helper to create demo teachers, courses, lessons, and one enrollment."""

from django.core.management.base import BaseCommand
from courses.models import Course
from accounts.models import User   # your custom user model
from enrollments.models import Enrollment
from lessons.models import Lesson # Import Lesson model

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
        self.stdout.write("Deleting existing courses, lessons, and teachers...")
        Course.objects.all().delete()
        User.objects.filter(role="teacher").delete()
        
        self.stdout.write("Creating new teachers and courses...")
        # Create each teacher and their course.
        for i, (name, course_title) in enumerate(zip(teachers, courses)):
            # Make a new teacher user with a simple default password.
            teacher = User.objects.create_user(
                username=name.lower(),
                password="password123",   # simple default password
                role="teacher",
                first_name=name
            )

            # Make a new course and link it to the teacher we just created.
            course = Course.objects.create(
                title=course_title,
                description=f"{course_title} taught by {name}.",
                teacher=teacher
            )

            # Create some lessons for the course
            for j in range(1, 4): # Create 3 lessons per course
                Lesson.objects.create(
                    course=course,
                    title=f"{course_title} - Lesson {j}",
                    content=f"This is the content for {course_title} - Lesson {j}.",
                    order=j
                )
                self.stdout.write(f"  Created lesson: {course_title} - Lesson {j}")

        self.stdout.write(self.style.SUCCESS("Database seeded successfully with teachers, courses, and lessons!"))

        # --- Enroll a student in a course ---
        self.stdout.write("Attempting to enroll a student...")
        student = User.objects.filter(role='student').first()
        course = Course.objects.first()

        if student and course:
            Enrollment.objects.get_or_create(student=student, course=course)
            self.stdout.write(self.style.SUCCESS(f"Enrolled student '{student.username}' in course '{course.title}'."))
        else:
            self.stdout.write(self.style.WARNING("Could not create enrollment. Make sure at least one student and one course exist."))