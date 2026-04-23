from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Mentors, Groups, Student

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ['date_joined']
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'first_name', 'last_name'),
        }),
    )

@admin.register(Mentors)
class MentorsAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'phone', 'birth_date')
    list_filter = ('department',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'phone')

@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'specialty', 'course', 'mentor')
    list_filter = ('course', 'specialty')
    search_fields = ('group_name', 'mentor__user__last_name')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'phone', 'birth_date')
    list_filter = ('group', 'group__course')
    search_fields = ('user__email', 'user__last_name', 'phone')
