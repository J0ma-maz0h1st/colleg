from django.contrib import admin
from .models import Tasks, Answers

@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'created_at', 'updated_at', 'deadline')
    list_filter = ('group', 'created_at')
    search_fields = ('title', 'description')


@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ('task', 'student', 'submitted_at', 'is_approved')
    list_filter = ('is_approved', 'submitted_at')
    search_fields = ('task__title', 'student__user__email')
