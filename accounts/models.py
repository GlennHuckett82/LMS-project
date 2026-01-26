
"""Custom user model with explicit role support for the LMS.

The built-in Django `AbstractUser` is extended with a `role` field so we can
quickly branch permission logic (student/teacher/admin) across the API and
frontend. Keeping the role here keeps checks consistent everywhere else.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

# This custom User model extends Django's built-in user system.
# It adds a 'role' field so we can easily tell if someone is a student, teacher, or admin.
class User(AbstractUser):
    # These are the possible roles a user can have in the LMS.
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    # The role field lets us assign a type to each user, which controls their permissions and access.
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

