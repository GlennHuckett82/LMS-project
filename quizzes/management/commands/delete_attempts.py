from django.core.management.base import BaseCommand
from quizzes.models import QuizAttempt

class Command(BaseCommand):
    help = 'Deletes all quiz attempts to allow re-taking quizzes during development.'

    def handle(self, *args, **options):
        self.stdout.write('Deleting all existing quiz attempts...')
        count, _ = QuizAttempt.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} quiz attempts.'))
