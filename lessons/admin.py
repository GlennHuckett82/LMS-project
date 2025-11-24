
from django.contrib import admin
from .models import Lesson

# This custom admin class lets you manage lessons in the Django admin site.
# It makes it easy to see, search, and filter lessons by title, course, and order.
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
	# Show these fields in the lesson list view for quick reference.
	list_display = ("title", "course", "order")
	# Enable searching by lesson title for convenience.
	search_fields = ("title",)
	# Add a filter so you can quickly find lessons by course.
	list_filter = ("course",)
