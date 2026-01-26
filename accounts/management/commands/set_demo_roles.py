"""Ensure demo users exist with the correct roles for quick testing."""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Ensure demo users have correct roles (demoTeacher -> teacher, demoAdmin -> admin). Creates users if missing."

    def handle(self, *args, **options):
        User = get_user_model()

        # Ensure demoTeacher exists and has role 'teacher'
        teacher_username = "demoTeacher"
        teacher_defaults = {
            "email": "demo@example.com",
            "role": "teacher",
        }
        teacher_user, created = User.objects.get_or_create(
            username=teacher_username,
            defaults=teacher_defaults,
        )
        if created:
            teacher_user.set_password("password")
            teacher_user.role = "teacher"
            teacher_user.save()
            self.stdout.write(self.style.SUCCESS(f"Created {teacher_username} with role=teacher and password='password'"))
        else:
            if teacher_user.role != "teacher":
                old_role = teacher_user.role
                teacher_user.role = "teacher"
                teacher_user.save(update_fields=["role"])
                self.stdout.write(self.style.SUCCESS(f"Updated {teacher_username} role: {old_role} -> teacher"))
            else:
                self.stdout.write(f"{teacher_username} already has role=teacher")

        # Ensure demoAdmin exists and has role 'admin' with staff/superuser
        admin_username = "demoAdmin"
        admin_defaults = {
            "email": "demo@example.com",
            "role": "admin",
            "is_staff": True,
            "is_superuser": True,
        }
        admin_user, created = User.objects.get_or_create(
            username=admin_username,
            defaults=admin_defaults,
        )
        if created:
            admin_user.set_password("password")
            admin_user.role = "admin"
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f"Created {admin_username} with role=admin, is_staff, is_superuser and password='password'"))
        else:
            changed = []
            if admin_user.role != "admin":
                changed.append(("role", admin_user.role, "admin"))
                admin_user.role = "admin"
            if not admin_user.is_staff:
                changed.append(("is_staff", admin_user.is_staff, True))
                admin_user.is_staff = True
            if not admin_user.is_superuser:
                changed.append(("is_superuser", admin_user.is_superuser, True))
                admin_user.is_superuser = True
            if changed:
                admin_user.save(update_fields=["role", "is_staff", "is_superuser"])
                changes = ", ".join([f"{f}: {o} -> {n}" for f, o, n in changed])
                self.stdout.write(self.style.SUCCESS(f"Updated {admin_username}: {changes}"))
            else:
                self.stdout.write(f"{admin_username} already configured as admin")

        self.stdout.write(self.style.SUCCESS("Demo roles ensured."))
