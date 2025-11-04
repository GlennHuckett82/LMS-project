from rest_framework import generics
from .models import User
from .serializers import UserSerializer

class UserCreate(generics.CreateAPIView):
    """
    A view for creating new users.

    This view uses Django Rest Framework's generic `CreateAPIView`.
    It's a pre-built class that handles the logic for creating a new object.
    We just need to tell it what model and serializer to use.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

