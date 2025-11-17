from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Lesson
from .serializers import LessonSerializer
from accounts.permissions import IsLessonTeacherOrAdmin
from django.db.models import Q

class LessonViewSet(viewsets.ModelViewSet):
	serializer_class = LessonSerializer
	permission_classes = [permissions.IsAuthenticated, IsLessonTeacherOrAdmin]

	def get_queryset(self):
		user = self.request.user
		base = Lesson.objects.select_related("course", "course__teacher").order_by("order")
		# Admin: all lessons
		if getattr(user, "role", None) == "admin":
			return base
		# Teacher: only lessons from their own courses
		if getattr(user, "role", None) == "teacher":
			return base.filter(course__teacher=user)
		# Student: only lessons from courses they are enrolled in
		if getattr(user, "role", None) == "student":
			return base.filter(course__enrollments__student=user).distinct()
		# Anonymous or unknown role: no access
		return base.none()

	def perform_create(self, serializer):
		user = self.request.user
		course = serializer.validated_data.get("course")
		if not user.is_authenticated:
			raise PermissionDenied("Authentication required.")
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
