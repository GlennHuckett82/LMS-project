from rest_framework import serializers
from .models import Lesson
from courses.models import Course

class LessonSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = ["id", "course", "title", "content", "order"]
