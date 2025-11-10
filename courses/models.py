from django.db import models
from django.conf import settings

class Course(models.Model):
    """
    Represents a single course in the Learning Management System.

    Each course has a title, a detailed description, and is associated with
    a specific teacher. This model forms the core of our educational content.
    """
    title = models.CharField(max_length=200, verbose_name="Course Title")
    description = models.TextField(verbose_name="Course Description")
    # A link to the custom User model from the 'accounts' app is needed.
    # The 'on_delete=models.CASCADE' part means that if a teacher's account is deleted,
    # all of their courses will be deleted as well. This keeps the database clean.
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},
        verbose_name="Teacher"
    )

    def __str__(self):
        """
        Returns a human-readable string representation of the course,
        which is helpful in the Django admin site.
        """
        return self.title

