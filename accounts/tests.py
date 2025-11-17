from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User


class RegistrationTests(APITestCase):
	"""Tests for user registration behavior and role defaults."""

	def setUp(self):
		self.register_url = reverse('user-create')  # maps to /api/accounts/register/

	def test_registration_defaults_to_student_role(self):
		data = {
			'username': 'studA',
			'email': 'studA@example.com',
			'password': 'StrongPass!123'
		}
		resp = self.client.post(self.register_url, data, format='json')
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		user = User.objects.get(username='studA')
		self.assertEqual(user.role, 'student')
		self.assertNotIn('password', resp.data)

	def test_registration_with_teacher_role(self):
		data = {
			'username': 'teachA',
			'email': 'teachA@example.com',
			'password': 'StrongPass!123',
			'role': 'teacher'
		}
		resp = self.client.post(self.register_url, data, format='json')
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		user = User.objects.get(username='teachA')
		self.assertEqual(user.role, 'teacher')
		self.assertNotIn('password', resp.data)

	def test_registration_with_admin_role_requires_manual_flags(self):
		data = {
			'username': 'adminCandidate',
			'email': 'adminCandidate@example.com',
			'password': 'StrongPass!123',
			'role': 'admin'
		}
		resp = self.client.post(self.register_url, data, format='json')
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		user = User.objects.get(username='adminCandidate')
		# Role saved but staff/superuser flags remain False until promoted.
		self.assertEqual(user.role, 'admin')
		self.assertFalse(user.is_staff)
		self.assertFalse(user.is_superuser)
