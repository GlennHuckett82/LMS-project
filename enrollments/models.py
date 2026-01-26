"""Enrollment model linking students to courses with a unique constraint."""

from django.db import models
from django.conf import settings
from courses.models import Course


class Enrollment(models.Model):
    """
    Represents a student's enrollment in a course.

    This model links a User (the student) to a Course, making it easy to track who is taking what.
    Each student can only enroll in a specific course once, thanks to the unique constraint below.
    """
    # The student who is enrolled in the course.
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Student'
    )
    # The course the student is enrolled in.
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Course'
    )
    # The date and time when the student enrolled.
    enrolled_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Enrolled At'
    )

    class Meta:
        # Prevent a student from enrolling in the same course more than once.
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='unique_enrollment')
        ]
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'
        ordering = ['id']

    def __str__(self):
        """
        Return a readable string showing which student is enrolled in which course.
        """
        return f"{self.student.username} enrolled in {self.course.title}"