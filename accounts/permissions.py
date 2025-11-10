from rest_framework.permissions import BasePermission

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
