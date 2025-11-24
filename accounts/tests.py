
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User

# These tests check that user registration works as expected, including role assignment.
# They help make sure students, teachers, and admins are created correctly and securely.
class RegistrationTests(APITestCase):
	"""
	Tests for user registration behavior and role defaults.
	Each test simulates a registration request and checks the resulting user data.
	"""

	def setUp(self):
		# Set up the registration URL for all tests. This is the endpoint for creating users.
		self.register_url = reverse('user-create')  # maps to /api/accounts/register/

	def test_registration_defaults_to_student_role(self):
		# If no role is provided, the user should be created as a student by default.
		data = {
			'username': 'studA',
			'email': 'studA@example.com',
			'password': 'StrongPass!123'
		}
		resp = self.client.post(self.register_url, data, format='json')
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		user = User.objects.get(username='studA')
		self.assertEqual(user.role, 'student')
		# Password should never be returned in the API response.
		self.assertNotIn('password', resp.data)

	def test_registration_with_teacher_role(self):
		# If the role is set to 'teacher', the user should be created as a teacher.
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
		# Creating an admin user should not automatically make them staff or superuser.
		# These flags must be set manually for security reasons.
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
