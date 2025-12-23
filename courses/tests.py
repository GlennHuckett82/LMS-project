from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Course
from accounts.models import User

# This test suite checks the Course API endpoints for correct behavior and permissions.
# It creates users with different roles and verifies that only the right people can create, update, or delete courses.
class CourseAPITests(APITestCase):
    """
    Test suite for the Course API endpoints.

    Sets up users with different roles and a sample course to test permission logic for all main actions.
    """
    def setUp(self):
        """
        Set up users and a course for testing.

        This method runs before each test, so every test starts with a clean database.
        Creates two teachers, one student, and one admin, plus a sample course.
        """
        # Create users with different roles.
        self.teacher1 = User.objects.create_user(username='teacher1', password='password123', role='teacher', email='teacher1@example.com')
        self.teacher2 = User.objects.create_user(username='teacher2', password='password123', role='teacher', email='teacher2@example.com')
        self.student = User.objects.create_user(username='student', password='password123', role='student', email='student@example.com')
        self.admin = User.objects.create_user(username='admin', password='password123', role='admin', email='admin@example.com', is_staff=True, is_superuser=True)

        # Create a course owned by teacher1.
        self.course = Course.objects.create(
            title="Introduction to Testing",
            description="A course about writing great tests.",
            teacher=self.teacher1
        )

        # Set up URLs for list/create and detail endpoints.
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

    def test_admin_create_course_requires_teacher(self):
        """Admin must specify a teacher id; missing should fail."""
        self.client.force_authenticate(user=self.admin)
        data = {'title': 'Admin Attempt', 'description': 'No teacher supplied'}
        resp = self.client.post(self.list_create_url, data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('teacher', resp.data)

    def test_admin_can_create_course_with_teacher(self):
        """Admin specifying a valid teacher id succeeds and assigns that teacher."""
        self.client.force_authenticate(user=self.admin)
        data = {
            'title': 'Admin Created',
            'description': 'With teacher',
            'teacher': self.teacher2.id
        }
        resp = self.client.post(self.list_create_url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        course = Course.objects.get(title='Admin Created')
        self.assertEqual(course.teacher, self.teacher2)

    def test_anyone_can_list_courses(self):
        """
        Verify that listing courses is open to everyone.
        """
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

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

    def test_my_courses_lists_only_own_courses_for_teacher(self):
        """Authenticated teacher should see only their own courses at /api/courses/my/."""
        # Give teacher2 their own course so both have at least one
        Course.objects.create(title="T2 Course", description="Owned by teacher2", teacher=self.teacher2)
        self.client.force_authenticate(user=self.teacher1)
        url = reverse('my-courses')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Response may be paginated or simple list; handle both
        payload = resp.data
        items = payload.get('results', payload)
        titles = {c['title'] for c in items}
        self.assertIn(self.course.title, titles)
        self.assertNotIn("T2 Course", titles)

    def test_student_cannot_access_my_courses(self):
        """Students should receive 403 Forbidden for /api/courses/my/."""
        self.client.force_authenticate(user=self.student)
        url = reverse('my-courses')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_cannot_access_my_courses(self):
        """Admins are not treated as teachers for /api/courses/my/."""
        self.client.force_authenticate(user=self.admin)
        url = reverse('my-courses')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
