
from django.contrib import admin
from .models import Course

# This custom admin class lets you manage courses in the Django admin site.
# It makes it easy to see, search, and filter courses by title and teacher.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	# Show these fields in the course list view for quick reference.
	list_display = ("title", "teacher")
	# Enable searching by course title and description for convenience.
	search_fields = ("title", "description")
	# Add a filter so you can quickly find courses by teacher.
	list_filter = ("teacher",)
