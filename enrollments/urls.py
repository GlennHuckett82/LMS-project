from django.urls import path
from .views import (
    StudentEnrollmentListView,
    EnrollmentCreateView,
    CourseRosterListView,
)

urlpatterns = [
    # Student's own enrollments
    path('my-enrollments/', StudentEnrollmentListView.as_view(), name='my-enrollments'),
    # Enroll in a course (student)
    path('courses/<int:course_pk>/enroll/', EnrollmentCreateView.as_view(), name='course-enroll'),
    # Course roster (teacher/admin)
    path('courses/<int:course_pk>/roster/', CourseRosterListView.as_view(), name='course-roster'),
]
