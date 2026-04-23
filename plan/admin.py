
from django.contrib import admin
from .models import Subjects, Schedule

@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('subjects_name', 'semestr', 'time_amount', 'control_type')
    list_filter = ('semestr', 'control_type')
    search_fields = ('subjects_name',)
    fieldsets = (
        (None, {
            'fields': ('subjects_name', 'time_amount')
        }),
        ('Оценка и период', {
            'fields': ('semestr', 'control_type'),
        }),
    )

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'lesson_number', 'group', 'subjects', 'classroom', 'lesson_type')
    list_filter = ('day_of_week', 'lesson_type', 'group', 'subjects')
    search_fields = ('classroom', 'mentor__user__last_name', 'subjects__subjects_name')
    ordering = ('day_of_week', 'lesson_number')

    list_select_related = ('group', 'subjects', 'mentor') 
