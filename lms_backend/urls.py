"""
URL configuration for lms_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Django admin site
    path('admin/', admin.site.urls),

    # Accounts API endpoints
    # Handles user registration, login, profile management, etc.
    path('api/accounts/', include('accounts.urls')),

    # Courses API endpoints
    # Provides list, create, retrieve, update, and delete operations for courses
    path('api/courses/', include('courses.urls')),

    # Enrollments API endpoints
    # Manages student enrollments in courses
    path('api/enrollments/', include('enrollments.urls')),

    # Lessons API endpoints
    # Manages lessons within courses
    path('api/lessons/', include('lessons.urls')),

    # JWT authentication endpoints
    # - Obtain: exchange username/password for access + refresh tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # - Refresh: get a new access token using a valid refresh token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # - Verify: check if a given token is valid
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]