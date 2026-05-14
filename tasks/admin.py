from django.contrib import admin
from .models import Tasks, Answers, Question, TestResult

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

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('text', 'category')
#     search_fields = ('text', 'category')

# @admin.register(TestResult)
# class TestResultAdmin(admin.ModelAdmin):
#     list_display = ('user', 'score', 'total_questions', 'start_time', 'end_time', 'date_taken')
#     list_filter = ('date_taken',)
#     search_fields = ('user__email',)