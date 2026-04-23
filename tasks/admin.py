from django.contrib import admin
from django.utils.html import format_html
from .models import Exercises, Solution

@admin.register(Exercises)
class ExercisesAdmin(admin.ModelAdmin):
    list_display = ('ex_name', 'subject', 'mentor', 'groups', 'appointment_date', 'due_date')
    list_filter = ('subject', 'groups', 'appointment_date')
    search_fields = ('ex_name', 'description', 'mentor__user__last_name')
    ordering = ('-appointment_date',)

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('student', 'exercise', 'submitted_at', 'display_file')
    list_filter = ('exercise__subject', 'exercise__groups', 'submitted_at')
    search_fields = ('student__user__last_name', 'exercise__ex_name')
    readonly_fields = ('submitted_at',)

    def display_file(self, obj):
        if obj.document:
            return format_html('<a href="{}" target="_blank">📄 Документ</a>', obj.document.url)
        if obj.photo:
            return format_html('<a href="{}" target="_blank">🖼️ Фото</a>', obj.photo.url)
        return "Нет файлов"
    
    display_file.short_description = 'Файл решения'
