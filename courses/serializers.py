from rest_framework import serializers
from .models import Course
from accounts.serializers import UserSerializer

class CourseSerializer(serializers.ModelSerializer):
    """
    A serializer for the Course model.

    This class defines how Course objects should be converted into a format
    like JSON for the API. It also specifies which fields to include.
    """
    # Show the teacher's details, not just their ID.
    # Using the UserSerializer here provides a nested representation
    # of the teacher, which is much more useful for the frontend.
    teacher = UserSerializer(read_only=True)

    class Meta:
        model = Course
        # These are the fields that will be included in the API representation.
        fields = ['id', 'title', 'description', 'teacher']
