from django.db import models
from django.conf import settings
from courses.models import Course

class Enrollment(models.Model):
    """
    My model to represent a student's enrollment in a course.
    
    This acts as a through table, linking a User (the student) to a Course.
    It ensures that a student can only enroll in a specific course once.
    """
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Student'
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Course'
    )
    enrolled_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Enrolled At'
    )

    class Meta:
        # I'm adding a unique constraint to prevent a student from enrolling
        # in the same course more than once.
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='unique_enrollment')
        ]
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'
        ordering = ['id']

    def __str__(self):
        """
        A string representation of the enrollment.
        """
        return f"{self.student.username} enrolled in {self.course.title}"