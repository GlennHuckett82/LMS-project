from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    A serializer for our custom User model.

    This class tells Django Rest Framework how to convert the User object
    to and from JSON. It's a key part of our API, handling data validation,
    creation, and updates.
    """
    class Meta:
        model = User
        # These are the fields that will be used for serialization.
        # We'll expose the user's id, username, email, and role.
        fields = ('id', 'username', 'email', 'password', 'role')
        # We want to make sure the password field is write-only.
        # This means it can be used when creating or updating a user,
        # but it won't be included when we fetch user data.
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        
        This method is called when a new user is being registered. We override
        it from the base ModelSerializer to handle password hashing. We can't
        just store the password as plain text; that would be a huge security risk!
        """
        # We use the create_user method which handles the password hashing for us.
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'student') # Default to 'student' if not provided
        )
        return user
