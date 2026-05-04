from django.contrib import admin
from .models import Course, Module, Enrollment, Schedule


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'mentor', 'price', 'level', 'is_published', 'students_enrolled')
    list_filter = ('is_published', 'level', 'direction')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    ordering = ('course', 'order')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'is_completed')
    list_filter = ('is_completed', 'course')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'date', 'start_time', 'is_online')
    list_filter = ('date', 'is_online')