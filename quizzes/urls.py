"""Routes for fetching quizzes, submitting attempts, and viewing results."""

from django.urls import path
from .views import QuizDetailView, QuizAttemptView, QuizResultView

urlpatterns = [
    path('<int:lesson_id>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('attempt/', QuizAttemptView.as_view(), name='quiz-attempt'),
    path('result/<int:id>/', QuizResultView.as_view(), name='quiz-result'),
]
