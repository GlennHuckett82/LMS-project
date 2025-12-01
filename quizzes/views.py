from rest_framework import generics, permissions
from .models import Quiz, QuizAttempt
from .serializers import QuizSerializer, QuizAttemptSerializer, QuizResultSerializer

# /api/quizzes/<lesson_id>/
class QuizDetailView(generics.RetrieveAPIView):
    """
    Provides the quiz for a specific lesson.
    """
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        lesson_id = self.kwargs.get('lesson_id')
        # Using get() will raise a 404 if the quiz doesn't exist, which is what we want.
        return Quiz.objects.get(lesson__id=lesson_id)

# /api/quizzes/attempt/
class QuizAttemptView(generics.CreateAPIView):
    """
    Allows a student to submit their answers for a quiz.
    """
    serializer_class = QuizAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        """
        Pass request to the serializer.
        """
        return {'request': self.request}

# /api/quizzes/result/<attempt_id>/
class QuizResultView(generics.RetrieveAPIView):
    """
    Shows the results of a specific quiz attempt.
    """
    serializer_class = QuizResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = QuizAttempt.objects.all()
    lookup_field = 'id' # Use 'id' from the URL to look up the attempt

    def get_queryset(self):
        """
        Ensure users can only see their own quiz results.
        """
        return self.queryset.filter(student=self.request.user)
