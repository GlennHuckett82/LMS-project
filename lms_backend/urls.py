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
from lessons.views import lesson_detail_view

urlpatterns = [
    # Django admin site
    path('admin/', admin.site.urls),

    # Lesson detail route for HTML lesson pages
    path('courses/<int:course_id>/lessons/<int:lesson_id>/',
         lesson_detail_view,
         name='lesson_detail'),

    # API endpoints
    path('api/accounts/', include('accounts.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/enrollments/', include('enrollments.urls')),
    path('api/lessons/', include('lessons.urls')),
    path('api/quizzes/', include('quizzes.urls')),

    # JWT authentication endpoints (Login is handled under accounts/urls.py)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]