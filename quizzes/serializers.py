"""Serializers covering quiz delivery, attempts, and graded results."""

from rest_framework import serializers
from .models import Quiz, Question, Choice, QuizAttempt, Answer

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        # Do not expose is_correct here so students cannot see the answer key from the API.
        fields = ['id', 'text']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'choices']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'lesson', 'questions']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'selected_choice']

class QuizAttemptSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = QuizAttempt
        fields = ['id', 'quiz', 'answers']
        read_only_fields = ['id']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        # Assuming student is from the request, will be added in the view
        student = self.context['request'].user

        # Calculate score
        total_questions = validated_data['quiz'].questions.count()
        correct_answers = 0
        for answer_data in answers_data:
            choice = answer_data['selected_choice']
            if choice.is_correct:
                correct_answers += 1
        
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

        attempt = QuizAttempt.objects.create(student=student, score=score, **validated_data)
        for answer_data in answers_data:
            Answer.objects.create(attempt=attempt, **answer_data)
            
        return attempt

# Serializers for displaying quiz results, including correct answers and explanations.

class CorrectChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text']

class QuestionResultSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    correct_choice = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'text', 'explanation', 'choices', 'correct_choice']

    def get_correct_choice(self, obj):
        try:
            correct_choice = obj.choices.get(is_correct=True)
            return CorrectChoiceSerializer(correct_choice).data
        except Choice.DoesNotExist:
            return None

class AnswerResultSerializer(serializers.ModelSerializer):
    question = QuestionResultSerializer(read_only=True)
    
    class Meta:
        model = Answer
        fields = ['question', 'selected_choice']

class QuizResultSerializer(serializers.ModelSerializer):
    """
    Serializer to show the results of a quiz attempt, including explanations.
    """
    answers = AnswerResultSerializer(many=True, read_only=True)
    quiz_title = serializers.CharField(source='quiz.title')

    class Meta:
        model = QuizAttempt
        fields = ['id', 'student', 'quiz_title', 'score', 'completed_at', 'answers']
