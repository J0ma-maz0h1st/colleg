from django.contrib import admin
from .models import Lesson, LessonFile


class LessonFileInline(admin.TabularInline):
    model = LessonFile
    extra = 1


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order', 'is_preview', 'duration_minutes')
    list_filter = ('is_preview', 'module__course')
    inlines = [LessonFileInline]
    ordering = ('module', 'order')