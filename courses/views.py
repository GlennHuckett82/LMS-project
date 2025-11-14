from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Course
from .serializers import CourseSerializer
from accounts.permissions import IsTeacherOrAdmin, IsOwnerOrAdmin
from rest_framework.exceptions import ValidationError

class CourseListCreateView(generics.ListCreateAPIView):
    """
    API view to list all courses or create a new one.

    - GET: Returns a list of all existing courses. Open to any user.
    - POST: Creates a new course. Restricted to users with the 'teacher' role.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        
        This method is overridden to apply different permissions for
        different actions. 'GET' requests (listing courses) are open to anyone,
        but 'POST' requests (creating a course) are restricted to teachers.
        """
        if self.request.method == 'POST':
            # Allow teachers and admins to create courses.
            return [IsAuthenticated(), IsTeacherOrAdmin()]
        return []

    def perform_create(self, serializer):
        """Assign teacher intelligently on course creation.

        Rules:
        - If the user is a teacher: they become the course teacher (ignore any provided teacher field).
        - If the user is an admin: they may optionally supply a "teacher" id for a valid teacher; otherwise
          the admin themselves is NOT set as teacher (must provide teacher id) to avoid mixing roles.
        """
        user = self.request.user
        # Teacher creating their own course.
        if getattr(user, 'role', None) == 'teacher':
            serializer.save(teacher=user)
            return

        # Admin path: accept teacher id if valid.
        if getattr(user, 'role', None) == 'admin':
            teacher_id = self.request.data.get('teacher')
            if teacher_id:
                from accounts.models import User  # local import to avoid circular issues at module load
                try:
                    teacher = User.objects.get(id=teacher_id, role='teacher')
                    serializer.save(teacher=teacher)
                    return
                except User.DoesNotExist:
                    pass
        # Fallback: no valid teacher supplied by admin.
        raise ValidationError({'teacher': 'Admin must supply a valid teacher id when creating a course.'})


class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a single course.

    - GET: Returns a single course. Open to any user.
    - PUT/PATCH: Updates a course. Restricted to the teacher who owns it or an admin.
    - DELETE: Deletes a course. Restricted to the teacher who owns it or an admin.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        
        I'm setting this up so that 'GET' requests are open to anyone, but any
        modifying actions ('PUT', 'PATCH', 'DELETE') are restricted to the
        course owner or an admin.
        """
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return []

