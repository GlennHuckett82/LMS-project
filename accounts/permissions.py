from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from rest_framework.exceptions import NotFound
from courses.models import Course
from lessons.models import Lesson

class IsAdmin(BasePermission):
    """
    Custom permission to only allow users with the 'admin' role.
    
    This class checks if the user making the request is authenticated and
    has their 'role' attribute set to 'admin'. This is how endpoints
    that should only be accessible by administrators will be protected.
    """
    def has_permission(self, request, view):
        # The user must be authenticated to have a role.
        # Then we check if their role is 'admin'.
        return request.user and request.user.is_authenticated and request.user.role == 'admin'

class IsTeacher(BasePermission):
    """
    Custom permission to only allow users with the 'teacher' role.
    
    Similar to IsAdmin, but this checks for the 'teacher' role. This will be used
    to lock down actions like creating or updating courses.
    """
    def has_permission(self, request, view):
        # Check for authentication and the 'teacher' role.
        return request.user and request.user.is_authenticated and request.user.role == 'teacher'

class IsStudent(BasePermission):
    """
    Custom permission to only allow users with the 'student' role.
    
    This is for actions that only students can perform, like enrolling in a course.
    """
    def has_permission(self, request, view):
        # Check for authentication and the 'student' role.
        return request.user and request.user.is_authenticated and request.user.role == 'student'

class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    
    I'm creating this to check if the user is either the 'teacher' of a course
    or has the 'admin' role. This is for object-level permissions, so I'll
    implement the `has_object_permission` method.
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
    Custom permission to only allow the teacher of a course or an admin.
    
    I'm creating this to check permissions at the view level, before an object
    has been fetched. It looks up the course from the URL and checks if the
    requesting user is either the course's teacher or an admin.
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
    Allow modification if the user is the lesson's course teacher or an admin.
    Read-only access is allowed for everyone.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, Lesson):
            return False
        if request.user and request.user.is_authenticated and getattr(request.user, "role", None) == 'admin':
            return True
        return obj.course.teacher == request.user
