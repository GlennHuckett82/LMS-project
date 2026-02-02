from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Initialise demo data: demo roles and seeded teachers, courses, and lessons."

    def handle(self, *args, **options):
        self.stdout.write("Running set_demo_roles...")
        call_command("set_demo_roles")

        self.stdout.write("Running courses.seed...")
        call_command("seed")

        self.stdout.write(self.style.SUCCESS("Demo data initialised (demo users, teachers, courses, lessons)."))
