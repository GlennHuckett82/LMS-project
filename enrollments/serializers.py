from rest_framework import serializers
from .models import Enrollment
from courses.serializers import CourseSerializer
from accounts.serializers import UserSerializer

class EnrollmentSerializer(serializers.ModelSerializer):
    """
    This serializer is used for creating and viewing enrollment records.

    It exposes the main fields you need to know about an enrollment, and keeps things simple for the API.
    """
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrolled_at']
        read_only_fields = ['student', 'course', 'enrolled_at']

class StudentEnrollmentSerializer(serializers.ModelSerializer):
    """
    This serializer lists all the courses a student is enrolled in.

    It's used for the 'my-enrollments' endpoint, and includes full course details by nesting the CourseSerializer.
    """
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['course', 'enrolled_at']

class CourseRosterSerializer(serializers.ModelSerializer):
    """
    This serializer lists all the students enrolled in a course.

    It's used for the teacher's 'course roster' view, and includes full student details by nesting the UserSerializer.
    """
    student = UserSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['student', 'enrolled_at']
