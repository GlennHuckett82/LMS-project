from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Course
from accounts.models import User

class CourseAPITests(APITestCase):
    """
    My test suite for the Course API endpoints.
    
    I'll set up a few users with different roles to test the permission logic
    for creating, updating, and deleting courses.
    """
    def setUp(self):
        """
        Set up the necessary users and a course for testing.
        
        This method runs before each test, giving me a clean slate.
        """
        # User setup
        self.teacher1 = User.objects.create_user(username='teacher1', password='password123', role='teacher', email='teacher1@example.com')
        self.teacher2 = User.objects.create_user(username='teacher2', password='password123', role='teacher', email='teacher2@example.com')
        self.student = User.objects.create_user(username='student', password='password123', role='student', email='student@example.com')
        self.admin = User.objects.create_user(username='admin', password='password123', role='admin', email='admin@example.com', is_staff=True, is_superuser=True)

        # Course setup, owned by teacher1
        self.course = Course.objects.create(
            title="Introduction to Testing",
            description="A course about writing great tests.",
            teacher=self.teacher1
        )

        # URL endpoints
        self.list_create_url = reverse('course-list-create')
        self.detail_url = reverse('course-detail', kwargs={'pk': self.course.pk})

    def test_unauthenticated_user_cannot_create_course(self):
        """
        Verify that unauthenticated users receive a 401 Unauthorized error.
        """
        data = {'title': 'New Course', 'description': 'A description.'}
        response = self.client.post(self.list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_student_cannot_create_course(self):
        """
        Verify that a student user receives a 403 Forbidden error.
        """
        self.client.force_authenticate(user=self.student)
        data = {'title': 'New Course', 'description': 'A description.'}
        response = self.client.post(self.list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_can_create_course(self):
        """
        Verify that a teacher can successfully create a course.
        """
        self.client.force_authenticate(user=self.teacher1)
        data = {'title': 'Advanced Django', 'description': 'Deep dive into Django.'}
        response = self.client.post(self.list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that the course was created and assigned to the correct teacher
        self.assertEqual(Course.objects.count(), 2)
        new_course = Course.objects.get(title='Advanced Django')
        self.assertEqual(new_course.teacher, self.teacher1)

    def test_anyone_can_list_courses(self):
        """
        Verify that listing courses is open to everyone.
        """
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_anyone_can_retrieve_course(self):
        """
        Verify that retrieving a single course is open to everyone.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.course.title)

    def test_owner_teacher_can_update_course(self):
        """
        Verify the course owner can update their course.
        """
        self.client.force_authenticate(user=self.teacher1)
        data = {'title': 'Updated Title'}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Updated Title')

    def test_other_teacher_cannot_update_course(self):
        """
        Verify a teacher cannot update a course they don't own.
        """
        self.client.force_authenticate(user=self.teacher2)
        data = {'title': 'Malicious Update'}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_any_course(self):
        """
        Verify an admin can update a course they don't own.
        """
        self.client.force_authenticate(user=self.admin)
        data = {'title': 'Admin Update'}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Admin Update')

    def test_student_cannot_update_course(self):
        """
        Verify a student cannot update any course.
        """
        self.client.force_authenticate(user=self.student)
        data = {'title': 'Student Update'}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_teacher_can_delete_course(self):
        """
        Verify the course owner can delete their course.
        """
        self.client.force_authenticate(user=self.teacher1)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)

    def test_other_teacher_cannot_delete_course(self):
        """
        Verify a teacher cannot delete a course they don't own.
        """
        self.client.force_authenticate(user=self.teacher2)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_any_course(self):
        """
        Verify an admin can delete a course they don't own.
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)
