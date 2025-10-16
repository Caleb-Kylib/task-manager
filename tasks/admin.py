from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	list_display = ('title', 'owner', 'is_completed', 'priority', 'created_at', 'completed_at', 'due_date')
	list_filter = ('is_completed', 'priority', 'created_at', 'due_date')
	search_fields = ('title', 'description', 'owner__username')
