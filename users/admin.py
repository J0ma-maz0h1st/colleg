from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Mentor, Group, Student
from django import forms

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        # Пароль нужно устанавливать через set_password, чтобы он захешировался
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm


    list_display = ('email', 'first_name', 'last_name', 'role', 'phone', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'role', 'phone')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    # Это поля для формы ДОБАВЛЕНИЯ нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'first_name', 'last_name', 'role', 'is_staff', 'is_active', 'phone'),
        }),
    )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'gpa', 'potential_points', 'is_frozen')
    list_filter = ('is_frozen', 'is_portfolio_public')
    search_fields = ('user__email', 'user__last_name')
    # Делаем очки потенциала только для чтения в списке, чтобы админ их не "нарисовал" случайно
    readonly_fields = ('potential_points',) 

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('user', 'education_place', 'internal_rating', 'is_verified', 'is_frozen')
    list_filter = ('is_verified', 'is_frozen')
    search_fields = ('user__email', 'user__last_name', 'skills')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'direction', 'mentor', 'course', 'student_count')
    filter_horizontal = ('students',)
    search_fields = ('name',)
    list_filter = ('direction', 'course')

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = "Студентов"