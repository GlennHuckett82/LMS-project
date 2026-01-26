"""Admin customization for the custom User model with role visibility."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# This custom admin class lets us manage User accounts in the Django admin site.
# It extends the default User admin to include our custom 'role' field, so you can easily see and edit user roles.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
	# Show these fields in the user list view for quick reference.
	list_display = ("username", "email", "role", "is_staff", "is_active")
	# Add filters so you can quickly find users by role or status.
	list_filter = ("role", "is_staff", "is_superuser", "is_active")
	# Enable searching by username and email for convenience.
	search_fields = ("username", "email")
	# Sort users by username by default.
	ordering = ("username",)

	# Add the custom 'role' field to the standard User admin fieldsets so it's editable in the admin forms.
	fieldsets = BaseUserAdmin.fieldsets + (
		(None, {"fields": ("role",)}),
	)
	add_fieldsets = BaseUserAdmin.add_fieldsets + (
		(None, {"fields": ("role",)}),
	)
