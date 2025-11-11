from rest_framework import serializers
from .models import Enrollment
from courses.serializers import CourseSerializer
from accounts.serializers import UserSerializer

class EnrollmentSerializer(serializers.ModelSerializer):
    """
    My basic serializer for creating and viewing an enrollment.
    """
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrolled_at']
        read_only_fields = ['student', 'course', 'enrolled_at']

class StudentEnrollmentSerializer(serializers.ModelSerializer):
    """
    My serializer for listing the courses a student is enrolled in.
    
    This will be used for the 'my-enrollments' endpoint. It nests the
    CourseSerializer to provide full details about each course.
    """
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['course', 'enrolled_at']

class CourseRosterSerializer(serializers.ModelSerializer):
    """
    My serializer for listing the students enrolled in a course.
    
    This will be used for the teacher's 'course roster' view. It nests the
    UserSerializer to provide details about each student.
    """
    student = UserSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['student', 'enrolled_at']
