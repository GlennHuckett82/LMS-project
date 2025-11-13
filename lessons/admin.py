from django.contrib import admin
from .models import Lesson

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
	list_display = ("title", "course", "order")
	search_fields = ("title",)
	list_filter = ("course",)
