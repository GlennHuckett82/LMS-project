from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from courses.models import Course
from lessons.models import Lesson
from .models import Quiz, Question, Choice, QuizAttempt


class QuizFlowTests(APITestCase):
	"""End-to-end tests for basic quiz retrieval, attempt submission, and result viewing."""

	def setUp(self):
		# Create a student and another user to verify access control on results
		self.student = User.objects.create_user(
			username='quiz_student', password='Pass!12345', role='student', email='quiz_student@example.com'
		)
		self.other_student = User.objects.create_user(
			username='quiz_other', password='Pass!12345', role='student', email='quiz_other@example.com'
		)

		# Minimal course/lesson/quiz graph
		course = Course.objects.create(title='Quiz Course', description='For quiz tests', teacher=self.student)
		lesson = Lesson.objects.create(course=course, title='Lesson with Quiz', content='Body', order=1)
		self.quiz = Quiz.objects.create(lesson=lesson, title='Sample Quiz')
		# Two questions, one correct choice each
		self.q1 = Question.objects.create(quiz=self.quiz, text='Q1?', explanation='Because.')
		self.q2 = Question.objects.create(quiz=self.quiz, text='Q2?', explanation='Also because.')
		self.q1_correct = Choice.objects.create(question=self.q1, text='Q1 correct', is_correct=True)
		self.q1_wrong = Choice.objects.create(question=self.q1, text='Q1 wrong', is_correct=False)
		self.q2_correct = Choice.objects.create(question=self.q2, text='Q2 correct', is_correct=True)
		self.q2_wrong = Choice.objects.create(question=self.q2, text='Q2 wrong', is_correct=False)

		self.detail_url = reverse('quiz-detail', kwargs={'lesson_id': lesson.id})
		self.attempt_url = reverse('quiz-attempt')
		# attempt id is only known after creation; result URL will be built in test

	def test_quiz_detail_requires_auth_and_returns_questions(self):
		# Unauthenticated should be rejected
		resp = self.client.get(self.detail_url)
		self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

		# Authenticated student can see quiz with questions and choices
		self.client.force_authenticate(user=self.student)
		resp = self.client.get(self.detail_url)
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertEqual(resp.data['id'], self.quiz.id)
		self.assertEqual(len(resp.data['questions']), 2)
		first_question = resp.data['questions'][0]
		self.assertIn('choices', first_question)
		self.assertGreaterEqual(len(first_question['choices']), 1)

	def test_student_can_submit_attempt_and_view_result(self):
		self.client.force_authenticate(user=self.student)
		payload = {
			'quiz': self.quiz.id,
			'answers': [
				{'question': self.q1.id, 'selected_choice': self.q1_correct.id},
				{'question': self.q2.id, 'selected_choice': self.q2_wrong.id},
			]
		}
		resp = self.client.post(self.attempt_url, payload, format='json')
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		attempt_id = resp.data.get('id') or QuizAttempt.objects.latest('id').id
		attempt = QuizAttempt.objects.get(id=attempt_id)
		# One out of two correct => 50%
		self.assertAlmostEqual(attempt.score, 50.0)

		# Student can view their own result
		result_url = reverse('quiz-result', kwargs={'id': attempt_id})
		resp_result = self.client.get(result_url)
		self.assertEqual(resp_result.status_code, status.HTTP_200_OK)
		self.assertEqual(resp_result.data['id'], attempt_id)
		self.assertEqual(resp_result.data['quiz_title'], self.quiz.title)
		self.assertEqual(len(resp_result.data['answers']), 2)

	def test_other_student_cannot_view_someone_elses_result(self):
		# Create an attempt as main student
		self.client.force_authenticate(user=self.student)
		payload = {
			'quiz': self.quiz.id,
			'answers': [
				{'question': self.q1.id, 'selected_choice': self.q1_correct.id},
			]
		}
		resp = self.client.post(self.attempt_url, payload, format='json')
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		attempt_id = resp.data.get('id') or QuizAttempt.objects.latest('id').id

		# Other student should receive 404 because queryset is filtered by student
		self.client.force_authenticate(user=self.other_student)
		result_url = reverse('quiz-result', kwargs={'id': attempt_id})
		resp_other = self.client.get(result_url)
		self.assertEqual(resp_other.status_code, status.HTTP_404_NOT_FOUND)
