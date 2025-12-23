
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User

# These tests check that user registration works as expected, including role assignment.
# They help make sure students, teachers, and admins are created correctly and securely.
class RegistrationTests(APITestCase):
	"""Registration behavior and role defaults."""

	def setUp(self):
		# Set up the registration URL for all tests. This is the endpoint for creating users.
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
		# Password should never be returned in the API response.
		self.assertNotIn('password', resp.data)

	def test_registration_with_teacher_role(self):
		"""Even if role='teacher' is sent, user stays a student for security."""
		data = {
			'username': 'teachA',
			'email': 'teachA@example.com',
			'password': 'StrongPass!123',
			'role': 'teacher'
		}
		resp = self.client.post(self.register_url, data, format='json')
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		user = User.objects.get(username='teachA')
		# Backend ignores requested elevated role and defaults to student.
		self.assertEqual(user.role, 'student')
		self.assertNotIn('password', resp.data)

	def test_registration_with_admin_role_requires_manual_flags(self):
		"""Self-registration cannot create admins; user is student with no flags."""
		data = {
			'username': 'adminCandidate',
			'email': 'adminCandidate@example.com',
			'password': 'StrongPass!123',
			'role': 'admin'
		}
		resp = self.client.post(self.register_url, data, format='json')
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		user = User.objects.get(username='adminCandidate')
		# Backend forces safe defaults: role becomes student, no elevated flags.
		self.assertEqual(user.role, 'student')
		self.assertFalse(user.is_staff)
		self.assertFalse(user.is_superuser)


class AuthMeTests(APITestCase):
	"""Tests for login and /accounts/me/ behavior for each role."""

	def setUp(self):
		self.login_url = reverse('token_obtain_pair')
		self.me_url = reverse('accounts_me')
		# Create one user of each role
		self.student = User.objects.create_user(
			username='stud_me', password='Pass!12345', role='student', email='stud_me@example.com'
		)
		self.teacher = User.objects.create_user(
			username='teach_me', password='Pass!12345', role='teacher', email='teach_me@example.com'
		)
		self.admin = User.objects.create_user(
			username='admin_me',
			password='Pass!12345',
			role='admin',
			email='admin_me@example.com',
			is_staff=True,
			is_superuser=True,
		)

	def _login_and_get_access(self, username: str, password: str) -> str:
		resp = self.client.post(self.login_url, {'username': username, 'password': password}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertIn('access', resp.data)
		self.assertIn('refresh', resp.data)
		return resp.data['access']

	def _get_me(self, access_token: str):
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
		resp = self.client.get(self.me_url)
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		return resp.data

	def test_student_login_and_me(self):
		access = self._login_and_get_access('stud_me', 'Pass!12345')
		data = self._get_me(access)
		self.assertEqual(data['username'], 'stud_me')
		self.assertEqual(data['role'], 'student')
		self.assertFalse(data['is_staff'])
		self.assertFalse(data['is_superuser'])

	def test_teacher_login_and_me(self):
		access = self._login_and_get_access('teach_me', 'Pass!12345')
		data = self._get_me(access)
		self.assertEqual(data['username'], 'teach_me')
		self.assertEqual(data['role'], 'teacher')
		self.assertFalse(data['is_staff'])
		self.assertFalse(data['is_superuser'])

	def test_admin_login_and_me(self):
		access = self._login_and_get_access('admin_me', 'Pass!12345')
		data = self._get_me(access)
		self.assertEqual(data['username'], 'admin_me')
		# Role field may be 'admin', but staff/superuser must be True
		self.assertEqual(data['role'], 'admin')
		self.assertTrue(data['is_staff'])
		self.assertTrue(data['is_superuser'])
