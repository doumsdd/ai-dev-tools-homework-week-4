from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "priority", "due_date", "completed", "created_at")
    list_filter = ("priority", "completed", "due_date")
    search_fields = ("title", "description")
    ordering = ("priority", "due_date")