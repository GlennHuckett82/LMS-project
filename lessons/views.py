from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Lesson
from .serializers import LessonSerializer
from accounts.permissions import IsLessonTeacherOrAdmin

class LessonViewSet(viewsets.ModelViewSet):
	queryset = Lesson.objects.select_related("course", "course__teacher").all().order_by("order")
	serializer_class = LessonSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsLessonTeacherOrAdmin]

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
