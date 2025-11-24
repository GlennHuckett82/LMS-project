
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Course
from .serializers import CourseSerializer
from accounts.permissions import IsTeacherOrAdmin, IsOwnerOrAdmin
from rest_framework.exceptions import ValidationError

class CourseListCreateView(generics.ListCreateAPIView):
    """
    API view to list all courses or create a new one.

    - GET: Anyone can list all existing courses.
    - POST: Only teachers and admins can create new courses.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """
        Set permissions for this view based on the request method.

        - GET: Open to anyone.
        - POST: Only authenticated teachers and admins can create courses.
        """
        if self.request.method == 'POST':
            # Allow teachers and admins to create courses.
            return [IsAuthenticated(), IsTeacherOrAdmin()]
        return []

    def perform_create(self, serializer):
        """
        Assign the correct teacher when creating a course.

        - If the user is a teacher: they become the course teacher (ignore any provided teacher field).
        - If the user is an admin: they must supply a valid teacher id; admin is not set as teacher.
        """
        user = self.request.user
        # If a teacher is creating the course, assign them as the teacher.
        if getattr(user, 'role', None) == 'teacher':
            serializer.save(teacher=user)
            return

        # If an admin is creating the course, use the provided teacher id.
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
        # If no valid teacher is supplied by admin, raise an error.
        raise ValidationError({'teacher': 'Admin must supply a valid teacher id when creating a course.'})


class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a single course.

    - GET: Anyone can view a course.
    - PUT/PATCH/DELETE: Only the teacher who owns the course or an admin can modify or delete it.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """
        Set permissions for this view based on the request method.

        - GET: Open to anyone.
        - PUT/PATCH/DELETE: Only authenticated course owners and admins can modify or delete.
        """
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return []

