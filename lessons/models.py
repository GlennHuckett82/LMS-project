
from django.db import models
from django.conf import settings
from courses.models import Course

# The Lesson model represents a single lesson within a course.
# Each lesson is linked to a course, has a title, some content, and an order value to control its position.
class Lesson(models.Model):
    # Connect this lesson to a specific course. If the course is deleted, all its lessons go too.
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    # The name of the lesson, shown to students and teachers.
    title = models.CharField(max_length=200)
    # The main content for the lesson (could be text, instructions, etc.).
    content = models.TextField()
    # The order of this lesson within the course. Lower numbers come first.
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        # When you print a lesson, show its title and which course it belongs to.
        return f"{self.title} (Course: {self.course.title})"

    class Meta:
        # Always sort lessons by their order value when querying.
        ordering = ["order"]
        # Make sure each lesson in a course has a unique order number.
        constraints = [
            models.UniqueConstraint(fields=["course", "order"], name="unique_lesson_order_per_course")
        ]

# The LessonProgress model tracks a student's completion status for a specific lesson.
# It links a user to a lesson and stores whether they have completed it.
class LessonProgress(models.Model):
    # Link to the user who is making progress. If the user is deleted, this progress record is also deleted.
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lesson_progress")
    # Link to the lesson being tracked. If the lesson is deleted, this progress record is also deleted.
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="progress")
    # Boolean field to mark the lesson as completed. Defaults to False.
    is_completed = models.BooleanField(default=False)
    # Timestamp for when the lesson was marked as complete.
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensure that a user can only have one progress entry per lesson.
        constraints = [
            models.UniqueConstraint(fields=["student", "lesson"], name="unique_student_lesson_progress")
        ]

    def __str__(self):
        # A string representation for the admin panel and debugging.
        return f"{self.student.username}'s progress on {self.lesson.title} - {'Completed' if self.is_completed else 'In Progress'}"
