
from django.urls import path
from .views import UserCreate
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# This file defines the API endpoints for user registration and authentication.
# Each path connects a URL to a view, making it easy to manage user accounts and JWT tokens.
urlpatterns = [
    # Endpoint for registering a new user (students, teachers, or admins).
    path('register/', UserCreate.as_view(), name='user-create'),
    # Endpoint for logging in and getting a JWT token.
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Endpoint for refreshing an existing JWT token.
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
