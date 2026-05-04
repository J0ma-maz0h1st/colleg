from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название курса")
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(verbose_name="Описание")
    short_description = models.CharField(max_length=300, blank=True)

    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_courses',
        limit_choices_to={'role': 'mentor'}
    )

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    thumbnail = models.ImageField(upload_to='courses/thumbnails/', null=True, blank=True)
    duration_hours = models.PositiveIntegerField(default=0)
    level = models.CharField(max_length=20, choices=[
        ('beginner', 'Начальный'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ])

    direction = models.CharField(max_length=100)  # Python, Web и т.д.

    students_enrolled = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['order']
        unique_together = ('course', 'order')
        verbose_name = "Модуль"
        verbose_name_plural = "Модули"

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
        limit_choices_to={'role': 'student'}
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-enrolled_at']
        verbose_name = "Запись на курс"
        verbose_name_plural = "Записи на курсы"


class Schedule(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='schedule')
    lesson = models.ForeignKey('lessons.Lesson', on_delete=models.CASCADE, related_name='schedule_entries')

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    meeting_link = models.URLField(blank=True, null=True)  # Zoom / Google Meet
    is_online = models.BooleanField(default=True)

    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ('lesson', 'date')
        verbose_name = "Расписание урока"
        verbose_name_plural = "Расписание уроков"

    def __str__(self):
        return f"{self.lesson.title} - {self.date}"