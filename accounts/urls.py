
from django.urls import path
from .views import UserCreate, MyTokenObtainPairView, me, AdminUserList, AdminUserDetail
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

# This file defines the API endpoints for user registration and authentication.
# Each path connects a URL to a view, making it easy to manage user accounts and JWT tokens.
urlpatterns = [
    # Endpoint for registering a new user (students, teachers, or admins).
    path('register/', UserCreate.as_view(), name='user-create'),
    # Endpoint for logging in and getting a JWT token.
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Endpoint for refreshing an existing JWT token.
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Endpoint to get current authenticated user's info including role.
    path('me/', me, name='accounts_me'),
    # Admin endpoints to list and update users
    path('users/', AdminUserList.as_view(), name='admin_users_list'),
    path('users/<int:user_id>/', AdminUserDetail.as_view(), name='admin_users_detail'),
]
