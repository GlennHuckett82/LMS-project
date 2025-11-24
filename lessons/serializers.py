
from rest_framework import serializers
from .models import Lesson
from courses.models import Course

# This serializer turns Lesson objects into JSON and back again.
# It's used by the API to send lesson data to the frontend and accept new lessons from users.
class LessonSerializer(serializers.ModelSerializer):
    # When creating or updating a lesson, this field lets you pick a course by its ID.
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Lesson
        # These are the fields that will be included in the API responses and requests.
        fields = ["id", "course", "title", "content", "order"]
