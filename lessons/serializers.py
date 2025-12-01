
from rest_framework import serializers
from .models import Lesson, LessonProgress
from courses.models import Course
from courses.serializers import CourseSerializer

# This serializer turns Lesson objects into JSON and back again.
# It's used by the API to send lesson data to the frontend and accept new lessons from users.
class LessonSerializer(serializers.ModelSerializer):
    # For read operations, show full course details. For write operations, allow picking a course by ID.
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )
    is_completed = serializers.SerializerMethodField()
    quiz_id = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        # These are the fields that will be included in the API responses and requests.
        fields = ["id", "course", "course_id", "title", "content", "order", "is_completed", "quiz_id"]

    def get_is_completed(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            student = request.user
            return LessonProgress.objects.filter(lesson=obj, student=student, is_completed=True).exists()
        return False

    def get_quiz_id(self, obj):
        if hasattr(obj, 'quiz') and obj.quiz:
            return obj.quiz.id
        return None

# Serializer for tracking student progress on lessons.
# This handles the data for marking a lesson as complete.
class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        # The fields to include in the API representation.
        fields = ["id", "student", "lesson", "is_completed", "completed_at"]
        read_only_fields = ["student", "completed_at"]
