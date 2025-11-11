from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from .models import Enrollment
from .serializers import EnrollmentSerializer, StudentEnrollmentSerializer, CourseRosterSerializer
from courses.models import Course
from accounts.permissions import IsStudent, IsCourseTeacherOrAdmin

class EnrollmentCreateView(generics.CreateAPIView):
    """
    My API view for a student to enroll in a course.
    
    This is a POST-only endpoint. A student sends a request here, and if they
    are authenticated and have the 'student' role, an enrollment record is created.
    """
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def create(self, request, *args, **kwargs):
        course_pk = self.kwargs.get('course_pk')
        course = get_object_or_404(Course, pk=course_pk)
        student = request.user

        try:
            # The unique_constraint on the model will prevent duplicates.
            Enrollment.objects.create(student=student, course=course)
            return Response({'detail': 'Successfully enrolled in the course.'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            # This happens if the unique_constraint is violated.
            return Response({'detail': 'You are already enrolled in this course.'}, status=status.HTTP_400_BAD_REQUEST)

class StudentEnrollmentListView(generics.ListAPIView):
    """
    My API view for a student to list their own enrollments.
    
    This is a GET-only endpoint that returns a list of courses the currently
    authenticated student is enrolled in, using a dedicated serializer for it.
    """
    serializer_class = StudentEnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the enrollments
        for the currently authenticated user.
        """
        user = self.request.user
        return Enrollment.objects.filter(student=user).select_related('course', 'course__teacher')

class CourseRosterListView(generics.ListAPIView):
    """
    My API view for a teacher to see the roster of students for their course.
    
    This is a GET-only endpoint, protected so that only the teacher who owns
    the course (or an admin) can view the list of enrolled students.
    """
    serializer_class = CourseRosterSerializer
    permission_classes = [IsAuthenticated, IsCourseTeacherOrAdmin]

    def get_queryset(self):
        """
        This view should return a list of all the enrollments for
        the course specified in the URL.
        """
        course_pk = self.kwargs.get('course_pk')
        return Enrollment.objects.filter(course__pk=course_pk).select_related('student')
