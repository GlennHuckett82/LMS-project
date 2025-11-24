
# Import necessary modules from Django REST Framework and local apps.
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Lesson
from .serializers import LessonSerializer
from accounts.permissions import IsLessonTeacherOrAdmin
from django.db.models import Q


# This viewset handles all CRUD operations for lessons.
# It enforces permissions so only the right users can access or modify lessons.
class LessonViewSet(viewsets.ModelViewSet):
	# Use the LessonSerializer for input/output formatting
	serializer_class = LessonSerializer
	# Only authenticated users with the right role can access lesson endpoints
	permission_classes = [permissions.IsAuthenticated, IsLessonTeacherOrAdmin]

	def get_queryset(self):
		"""
		Returns the set of lessons the current user is allowed to see.
		- Admins see all lessons.
		- Teachers see lessons for their own courses.
		- Students see lessons for courses they're enrolled in.
		- Anyone else gets nothing.
		"""
		user = self.request.user
		base = Lesson.objects.select_related("course", "course__teacher").order_by("order")
		# If the user is an admin, show all lessons
		if getattr(user, "role", None) == "admin":
			return base
		# If the user is a teacher, show only lessons for their courses
		if getattr(user, "role", None) == "teacher":
			return base.filter(course__teacher=user)
		# If the user is a student, show lessons for courses they're enrolled in
		if getattr(user, "role", None) == "student":
			return base.filter(course__enrollments__student=user).distinct()
		# If the user is anonymous or has no valid role, show nothing
		return base.none()

	def perform_create(self, serializer):
		"""
		Handles creation of a new lesson.
		Only admins or the teacher of the course can create lessons for that course.
		"""
		user = self.request.user
		course = serializer.validated_data.get("course")
		if not user.is_authenticated:
			raise PermissionDenied("Authentication required.")
		# Allow creation if user is admin or the teacher for the course
		if getattr(user, "role", None) == "admin" or course.teacher == user:
			serializer.save()
		else:
			raise PermissionDenied("Only the course teacher or admin can create lessons for this course.")

	def perform_update(self, serializer):
		"""
		Handles updates to an existing lesson.
		Only admins or the teacher of the course can modify lessons for that course.
		"""
		user = self.request.user
		course = serializer.instance.course
		# Allow update if user is admin or the teacher for the course
		if getattr(user, "role", None) == "admin" or course.teacher == user:
			serializer.save()
		else:
			raise PermissionDenied("Only the course teacher or admin can modify this lesson.")
