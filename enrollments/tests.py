from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Enrollment
from courses.models import Course
from accounts.models import User

class EnrollmentAPITests(APITestCase):
    """
    My test suite for the Enrollment API endpoints.
    
    I'll set up users with different roles to test the permissions for
    enrolling in courses and viewing enrollment lists.
    """
    def setUp(self):
        """
        Set up the necessary users, courses, and an initial enrollment.
        """
        # User setup
        self.teacher1 = User.objects.create_user(username='teacher1', password='password123', role='teacher', email='teacher1@example.com')
        self.teacher2 = User.objects.create_user(username='teacher2', password='password123', role='teacher', email='teacher2@example.com')
        self.student1 = User.objects.create_user(username='student1', password='password123', role='student', email='student1@example.com')
        self.student2 = User.objects.create_user(username='student2', password='password123', role='student', email='student2@example.com')
        self.admin = User.objects.create_user(username='admin', password='password123', role='admin', email='admin@example.com', is_staff=True, is_superuser=True)

        # Course setup
        self.course1 = Course.objects.create(title="Course One", description="Description one.", teacher=self.teacher1)
        self.course2 = Course.objects.create(title="Course Two", description="Description two.", teacher=self.teacher2)

        # Initial enrollment for student1 in course1
        self.enrollment = Enrollment.objects.create(student=self.student1, course=self.course1)

        # URL endpoints
        self.enroll_url = reverse('course-enroll', kwargs={'course_pk': self.course2.pk})
        self.my_enrollments_url = reverse('my-enrollments')
        self.roster_url = reverse('course-roster', kwargs={'course_pk': self.course1.pk})

    # --- Enrollment Creation Tests ---
    def test_student_can_enroll(self):
        """
        Verify that a student can successfully enroll in a course.
        """
        self.client.force_authenticate(user=self.student2)
        response = self.client.post(self.enroll_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Enrollment.objects.filter(student=self.student2, course=self.course2).exists())

    def test_student_cannot_enroll_twice(self):
        """
        Verify that a student cannot enroll in the same course twice.
        """
        self.client.force_authenticate(user=self.student1)
        # student1 is already enrolled in course1 in setUp
        enroll_in_course1_url = reverse('course-enroll', kwargs={'course_pk': self.course1.pk})
        response = self.client.post(enroll_in_course1_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_teacher_cannot_enroll(self):
        """
        Verify that a teacher receives a 403 Forbidden error when trying to enroll.
        """
        self.client.force_authenticate(user=self.teacher1)
        response = self.client.post(self.enroll_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- Student's Enrollment List Tests ---
    def test_student_can_view_own_enrollments(self):
        """
        Verify a student can see a list of their enrolled courses.
        """
        self.client.force_authenticate(user=self.student1)
        response = self.client.get(self.my_enrollments_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['course']['title'], self.course1.title)

    def test_unauthenticated_cannot_view_enrollments(self):
        """
        Verify unauthenticated users get a 401 error for 'my-enrollments'.
        """
        response = self.client.get(self.my_enrollments_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- Course Roster Tests ---
    def test_owner_teacher_can_view_roster(self):
        """
        Verify the course owner can view the list of enrolled students.
        """
        self.client.force_authenticate(user=self.teacher1)
        response = self.client.get(self.roster_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['student']['username'], self.student1.username)

    def test_other_teacher_cannot_view_roster(self):
        """
        Verify a teacher cannot view the roster for a course they don't own.
        """
        self.client.force_authenticate(user=self.teacher2)
        response = self.client.get(self.roster_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_view_roster(self):
        """
        Verify a student cannot view the roster for any course.
        """
        self.client.force_authenticate(user=self.student1)
        response = self.client.get(self.roster_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_view_any_roster(self):
        """
        Verify an admin can view the roster for any course.
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.roster_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
