"""Endpoints for creating enrollments, listing a student's courses, and course rosters."""

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
    API view for a student to enroll in a course.

    POST-only endpoint: authenticated students can enroll in a course by sending a request here.
    If they're already enrolled, they'll get a helpful error message.
    """
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def create(self, request, *args, **kwargs):
        # Get the course ID from the URL and fetch the course object.
        course_pk = self.kwargs.get('course_pk')
        course = get_object_or_404(Course, pk=course_pk)
        student = request.user

        try:
            # Try to create the enrollment. If the student is already enrolled, the unique constraint will raise an error.
            Enrollment.objects.create(student=student, course=course)
            return Response({'detail': 'Successfully enrolled in the course.'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            # If the student is already enrolled, return a friendly error message.
            return Response({'detail': 'You are already enrolled in this course.'}, status=status.HTTP_400_BAD_REQUEST)

class StudentEnrollmentListView(generics.ListAPIView):
    """
    API view for a student to list their own enrollments.

    GET-only endpoint: returns a list of courses the authenticated student is enrolled in.
    Uses a dedicated serializer for clean, useful output.
    """
    serializer_class = StudentEnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return all enrollments for the currently authenticated user.
        This makes it easy for students to see what courses they're taking.
        """
        user = self.request.user
        return Enrollment.objects.filter(student=user).select_related('course', 'course__teacher')

class CourseRosterListView(generics.ListAPIView):
    """
    API view for a teacher to see the roster of students for their course.

    GET-only endpoint: only the teacher who owns the course (or an admin) can view the list of enrolled students.
    This helps teachers manage their classes and see who's enrolled.
    """
    serializer_class = CourseRosterSerializer
    permission_classes = [IsAuthenticated, IsCourseTeacherOrAdmin]

    def get_queryset(self):
        """
        Return all enrollments for the course specified in the URL.
        This lets teachers see every student enrolled in their course.
        """
        course_pk = self.kwargs.get('course_pk')
        return Enrollment.objects.filter(course__pk=course_pk).select_related('student')
