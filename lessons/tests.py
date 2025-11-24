from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from courses.models import Course
from enrollments.models import Enrollment
from lessons.models import Lesson


class LessonVisibilityTests(APITestCase):
	"""
	Test suite to make sure lesson content is only accessible to enrolled students, the course teacher, or an admin.

	These tests check that permissions are enforced for reading and updating lessons, so only the right users can access or modify lesson content.
	"""

	def setUp(self):
		# Create users for each role: teacher, enrolled student, not enrolled student, and admin.
		self.teacher = User.objects.create_user(username='teacherX', password='Pass!12345', role='teacher', email='teacherX@example.com')
		self.student_enrolled = User.objects.create_user(username='studEn', password='Pass!12345', role='student', email='studEn@example.com')
		self.student_not_enrolled = User.objects.create_user(username='studNo', password='Pass!12345', role='student', email='studNo@example.com')
		self.admin = User.objects.create_user(username='adminX', password='Pass!12345', role='admin', email='adminX@example.com', is_staff=True, is_superuser=True)

		# Create a course and enroll one student.
		self.course = Course.objects.create(title='Visibility Course', description='Test visibility.', teacher=self.teacher)
		Enrollment.objects.create(student=self.student_enrolled, course=self.course)

		# Create two lessons for the course.
		self.lesson1 = Lesson.objects.create(course=self.course, title='L1', content='Content 1', order=1)
		self.lesson2 = Lesson.objects.create(course=self.course, title='L2', content='Content 2', order=2)

		# Set up detail URLs for each lesson.
		self.detail_url_l1 = reverse('lesson-detail', kwargs={'pk': self.lesson1.pk})
		self.detail_url_l2 = reverse('lesson-detail', kwargs={'pk': self.lesson2.pk})

	def test_enrolled_student_can_read_lessons(self):
		self.client.force_authenticate(user=self.student_enrolled)
		resp = self.client.get(self.detail_url_l1)
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertEqual(resp.data['title'], 'L1')

	def test_not_enrolled_student_cannot_read_lessons(self):
		self.client.force_authenticate(user=self.student_not_enrolled)
		resp = self.client.get(self.detail_url_l1)
		# Queryset filtering causes 404 (not found) rather than 403.
		self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

	def test_teacher_can_read_own_course_lessons(self):
		self.client.force_authenticate(user=self.teacher)
		resp = self.client.get(self.detail_url_l2)
		self.assertEqual(resp.status_code, status.HTTP_200_OK)

	def test_admin_can_read_any_lesson(self):
		self.client.force_authenticate(user=self.admin)
		resp = self.client.get(self.detail_url_l1)
		self.assertEqual(resp.status_code, status.HTTP_200_OK)

	def test_non_enrolled_student_cannot_update_lesson(self):
		self.client.force_authenticate(user=self.student_not_enrolled)
		resp = self.client.patch(self.detail_url_l1, {'title': 'Hack'})
		self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

	def test_teacher_can_update_lesson(self):
		self.client.force_authenticate(user=self.teacher)
		resp = self.client.patch(self.detail_url_l1, {'title': 'Updated L1'})
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.lesson1.refresh_from_db()
		self.assertEqual(self.lesson1.title, 'Updated L1')

	def test_admin_can_update_lesson(self):
		self.client.force_authenticate(user=self.admin)
		resp = self.client.patch(self.detail_url_l2, {'title': 'Admin Updated L2'})
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.lesson2.refresh_from_db()
		self.assertEqual(self.lesson2.title, 'Admin Updated L2')
