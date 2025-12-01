
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LessonViewSet, lesson_detail_view, LessonProgressView

# Set up a router for the LessonViewSet, which handles all lesson-related API endpoints.
# This makes it easy to add, list, update, and delete lessons using RESTful routes.
router = DefaultRouter()
router.register(r"", LessonViewSet, basename="lesson")

# The urlpatterns connect the router's URLs to the app, so Django knows how to route lesson API requests.
urlpatterns = [
    path(
        'courses/<int:course_id>/lessons/<int:lesson_id>/',
        lesson_detail_view,
        name='lesson_detail'
    ),
    path("lessons/progress/", LessonProgressView.as_view(), name="lesson-progress"),
    path("", include(router.urls)),
]