
from rest_framework import generics
from .models import User
from .serializers import UserSerializer

# This view lets users register for the LMS (students, teachers, or admins).
# It uses DRF's CreateAPIView, which handles all the details of creating a new user record.
class UserCreate(generics.CreateAPIView):
    """
    API view for creating new users.

    Uses Django Rest Framework's generic CreateAPIView, so you don't have to write the logic yourself.
    Just specify the model and serializer, and DRF takes care of the rest.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

