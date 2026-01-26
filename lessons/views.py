"""Lesson endpoints and views for CRUD plus progress tracking."""

# Import necessary modules from Django REST Framework and local apps.
from rest_framework import viewsets, permissions, generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Lesson, LessonProgress
from .serializers import LessonSerializer, LessonProgressSerializer
from accounts.permissions import IsLessonTeacherOrAdmin, IsStudent
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

# This viewset handles all CRUD operations for lessons.
# It enforces permissions so only the right users can access or modify lessons.

class LessonViewSet(viewsets.ModelViewSet):
	serializer_class = LessonSerializer
	permission_classes = [permissions.IsAuthenticated, IsLessonTeacherOrAdmin]
	pagination_class = None

	def get_queryset(self):
		"""
		Returns the set of lessons the current user is allowed to see.
		- Admins see all lessons.
		- Teachers see lessons for their own courses.
		- Students see lessons for courses they're enrolled in.
		- Anyone else gets nothing.
		"""
		user = self.request.user
		print(f"DEBUG: User in LessonViewSet get_queryset: {user.username}, ID: {user.id}, Role: {getattr(user, 'role', 'N/A')}")

		base = Lesson.objects.select_related("course", "course__teacher").order_by("order")
		if getattr(user, "role", None) == "admin":
			print("DEBUG: User is admin, returning all lessons.")
			return base
		if getattr(user, "role", None) == "teacher":
			print(f"DEBUG: User is teacher, filtering by courses for teacher {user.username}.")
			return base.filter(course__teacher=user)
		if getattr(user, "role", None) == "student":
			print(f"DEBUG: User is student, filtering by enrolled courses for student {user.username}.")
			queryset = base.filter(course__enrollments__student=user).distinct()
			print(f"DEBUG: Student queryset contains {queryset.count()} lessons.")
			for lesson_item in queryset:
				print(f"  - Lesson ID: {lesson_item.id}, Title: {lesson_item.title}, Course: {lesson_item.course.title}")
			return queryset
		print("DEBUG: User has no recognized role, returning empty queryset.")
		return base.none()

	def perform_create(self, serializer):
		user = self.request.user
		course = serializer.validated_data.get("course")
		if not user.is_authenticated:
			raise PermissionDenied("Authentication required.")
		# Only course owners or admins can add lessons; enforce here even though permissions are set on the viewset.
		if getattr(user, "role", None) == "admin" or course.teacher == user:
			serializer.save()
		else:
			raise PermissionDenied("Only the course teacher or admin can create lessons for this course.")

	def perform_update(self, serializer):
		user = self.request.user
		course = serializer.instance.course
		if getattr(user, "role", None) == "admin" or course.teacher == user:
			serializer.save()
		else:
			raise PermissionDenied("Only the course teacher or admin can modify this lesson.")

class LessonProgressView(generics.CreateAPIView):
    """
    API view for students to mark a lesson as complete.
    """
    serializer_class = LessonProgressSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def create(self, request, *args, **kwargs):
        lesson_id = request.data.get("lesson")
        if not lesson_id:
            return Response({"lesson": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)

        lesson = get_object_or_404(Lesson, id=lesson_id)

        # Check if the student is enrolled in the course this lesson belongs to
        if not request.user.enrollments.filter(course=lesson.course).exists():
            return Response({"detail": "You are not enrolled in the course for this lesson."}, status=status.HTTP_403_FORBIDDEN)

        progress, created = LessonProgress.objects.update_or_create(
            student=request.user,
            lesson=lesson,
            defaults={'is_completed': True}
        )
        
        serializer = self.get_serializer(progress)
        headers = self.get_success_headers(serializer.data)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code, headers=headers)


def lesson_detail_view(request, course_id, lesson_id):
	# Debug: Print lesson_id and course_id to verify correct values
	print(f"Requested lesson_id: {lesson_id}, course_id: {course_id}")
	lesson = get_object_or_404(Lesson, id=lesson_id, course__id=course_id)
	# Debug: Print lesson title and content to verify correct lesson
	print(f"Loaded lesson: {lesson.title}")
	context = {
		'lesson': lesson,
		'lesson_title': lesson.title,
		'lesson_content': lesson.content,
	}
	return render(request, 'lessons/lesson_detail.html', context)
