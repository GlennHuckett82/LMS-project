from django.urls import path
from .views import CourseListCreateView, CourseRetrieveUpdateDestroyView
from enrollments.views import EnrollmentCreateView, CourseRosterListView

# I'm defining the URL patterns for the courses app here.
urlpatterns = [
    # This path maps to the CourseListCreateView, which handles listing all courses (GET)
    # and creating a new course (POST).
    path('', CourseListCreateView.as_view(), name='course-list-create'),
    
    # This path handles retrieving, updating, or deleting a single course.
    # The '<int:pk>' part captures the primary key (the ID) of the course from the URL.
    path('<int:pk>/', CourseRetrieveUpdateDestroyView.as_view(), name='course-detail'),

    # This path is for a student to enroll in a specific course.
    path('<int:course_pk>/enroll/', EnrollmentCreateView.as_view(), name='course-enroll'),

    # This path is for a teacher to view the roster of students for their course.
    path('<int:course_pk>/students/', CourseRosterListView.as_view(), name='course-roster'),
]
