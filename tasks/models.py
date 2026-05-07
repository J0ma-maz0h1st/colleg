from django.db import models
from users.models import User, Mentor, Student, Group


class Tasks(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название задачи")
    description = models.TextField(verbose_name="Описание задачи")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='tasks', verbose_name="Группа")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    deadline = models.DateTimeField(verbose_name="Дедлайн", null=True, blank=True)
    file = models.FileField(upload_to='tasks/files/', null=True, blank=True, verbose_name="Прикрепленный файл")
    photo = models.ImageField(upload_to='tasks/photos/', null=True, blank=True, verbose_name="Прикрепленное фото")

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

class Answers(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name='answers', verbose_name="Задача")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='answers', verbose_name="Студент")
    content = models.TextField(verbose_name="Ответ студента")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")
    is_approved = models.BooleanField(default=False, verbose_name="Одобрено преподавателем")

    file = models.FileField(upload_to='answers/files/', null=True, blank=True, verbose_name="Прикрепленный файл")
    photo = models.ImageField(upload_to='answers/photos/', null=True, blank=True, verbose_name="Прикрепленное фото")

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"