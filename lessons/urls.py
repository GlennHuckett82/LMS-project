
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LessonViewSet

# Set up a router for the LessonViewSet, which handles all lesson-related API endpoints.
# This makes it easy to add, list, update, and delete lessons using RESTful routes.
router = DefaultRouter()
router.register(r"", LessonViewSet, basename="lesson")

# The urlpatterns connect the router's URLs to the app, so Django knows how to route lesson API requests.
urlpatterns = [
    path("", include(router.urls)),
]
