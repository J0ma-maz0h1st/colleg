from django.contrib import admin
from .models import Course, Direction

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'direction', 'type', 'level', 'cost', 'current_students_count', 'max_students_count')
    list_filter = ('direction', 'type', 'level')
    search_fields = ('name', 'description')
    readonly_fields = ('current_students_count',)

@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at', 'photo')
    search_fields = ('name', 'description', 'photo')
