from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Course
from .serializers import CourseSerializer
from accounts.permissions import IsTeacher, IsOwnerOrAdmin

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
            return [IsAuthenticated(), IsTeacher()]
        return []

    def perform_create(self, serializer):
        """
        Called when a new course is being created.

        This is overridden to automatically assign the currently logged-in
        teacher as the teacher of the new course. The frontend doesn't need
        to send the teacher's ID; it's handled securely on the backend.
        """
        serializer.save(teacher=self.request.user)


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

