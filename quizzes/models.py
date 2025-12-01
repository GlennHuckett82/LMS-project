from django.db import models
from django.conf import settings
from lessons.models import Lesson

# Represents a quiz, which is a collection of questions associated with a lesson.
class Quiz(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title

# Represents a single question within a quiz.
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(help_text="The question text.")
    explanation = models.TextField(blank=True, help_text="Explanation for why the correct answer is right.")

    def __str__(self):
        return self.text[:50]

# Represents a multiple-choice option for a question.
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False, help_text="Is this the correct answer?")

    def __str__(self):
        return f"{self.question.text[:30]} - {self.text[:30]}"

# Records a student's overall attempt at a quiz.
class QuizAttempt(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.FloatField(help_text="The final score as a percentage (e.g., 85.7).")
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username}'s attempt on {self.quiz.title}"

# Records the specific answer a student gave for a single question within an attempt.
class Answer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"Answer for '{self.question.text[:20]}...' in attempt {self.attempt.id}"

