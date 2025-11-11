from django.urls import path
from .views import StudentEnrollmentListView

# I'm defining the URL patterns for the enrollments app here.
urlpatterns = [
    # This path maps to the StudentEnrollmentListView, which allows a student
    # to see a list of all the courses they are enrolled in.
    path('my-enrollments/', StudentEnrollmentListView.as_view(), name='my-enrollments'),
]
