
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from rest_framework.exceptions import NotFound
from courses.models import Course
from lessons.models import Lesson
from enrollments.models import Enrollment

# This file contains custom permission classes for the LMS API.
# Each class makes it easy to control who can access or modify different resources, using clear role-based rules.

class IsAdmin(BasePermission):
    """
    Only allow access to users with the 'admin' role.

    Use this for endpoints that should be locked down for administrators only.
    Checks authentication and the user's role.
    """
    def has_permission(self, request, view):
        # The user must be authenticated to have a role.
        # Then we check if their role is 'admin'.
        return request.user and request.user.is_authenticated and request.user.role == 'admin'

class IsTeacher(BasePermission):
    """
    Only allow access to users with the 'teacher' role.

    Use this for actions like creating or updating courses, so only teachers can do them.
    """
    def has_permission(self, request, view):
        # Check for authentication and the 'teacher' role.
        return request.user and request.user.is_authenticated and request.user.role == 'teacher'

class IsStudent(BasePermission):
    """
    Only allow access to users with the 'student' role.

    Use this for endpoints that only students should be able to use, like enrolling in courses.
    """
    def has_permission(self, request, view):
        # Check for authentication and the 'student' role.
        return request.user and request.user.is_authenticated and request.user.role == 'student'

class IsTeacherOrAdmin(BasePermission):
    """
    Allow access if the user is either a teacher or an admin.

    Use this for actions where both teachers and admins should be allowed, like creating courses.
    This keeps the code clean and makes the intent obvious.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                request.user.role == 'teacher' or request.user.role == 'admin'
            )
        )

class IsOwnerOrAdmin(BasePermission):
    """
    Only allow editing if the user is the owner (teacher) of the object or an admin.

    Use this for object-level permissions, like editing a course. Admins can always edit; teachers can edit their own courses.
    """
    def has_object_permission(self, request, view, obj):
        # Admins can do anything.
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        
        # Otherwise, the user must be the teacher of the course.
        # The 'obj' here is the Course instance.
        return obj.teacher == request.user

class IsCourseTeacherOrAdmin(BasePermission):
    """
    Only allow access if the user is the teacher of the course or an admin.

    Checks permissions before the object is fetched, using the course ID from the URL.
    """
    def has_permission(self, request, view):
        # The user must be authenticated to proceed.
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admins are always allowed.
        if request.user.role == 'admin':
            return True
        
        # Get the course from the URL.
        course_pk = view.kwargs.get('course_pk')
        if not course_pk:
            return False # Should not happen if URL is configured correctly.

        try:
            course = Course.objects.get(pk=course_pk)
        except Course.DoesNotExist:
            # The view will handle the 404, but we deny permission.
            return False

        # Check if the user is the teacher of the course.
        return course.teacher == request.user

class IsLessonTeacherOrAdmin(BasePermission):
    """
    Allow editing if the user is the teacher of the lesson's course or an admin.
    Anyone can read lessons, but only teachers and admins can modify them.
    """
    def has_permission(self, request, view):
        # Require authentication for any write; reads will be further checked per-object/view.
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, Lesson):
            return False
        # Admin can read/write any lesson.
        if request.user and request.user.is_authenticated and getattr(request.user, "role", None) == 'admin':
            return True
        # Course teacher can read/write their lessons.
        if obj.course.teacher == request.user:
            return True
        # For SAFE methods (read), allow if the user is enrolled in the course.
        if request.method in SAFE_METHODS:
            return Enrollment.objects.filter(student=request.user, course=obj.course).exists()
        return False
