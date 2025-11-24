
from django.db import models
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
