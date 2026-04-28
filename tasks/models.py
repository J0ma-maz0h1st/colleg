from django.db import models
from plan.models import Subjects
from users.models import Mentor, Group, Student

class Exercises(models.Model):
    ex_name = models.CharField(max_length=30, verbose_name='Название задания')
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name='exercises', verbose_name='Предмет')
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='assigned_exercises', verbose_name='Препод')
    groups = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='exercises', verbose_name='Группы')
    appointment_date = models.DateField(auto_now_add=True)
    due_date = models.DateTimeField(help_text='Время сдачи задания')
    description = models.TextField(max_length=635)

    def __str__(self):
        return self.ex_name

class Solution(models.Model):
    exercise = models.ForeignKey(Exercises, on_delete=models.CASCADE, related_name='solutions', verbose_name='Задание')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='solutions', verbose_name='Студент')
    photo = models.ImageField(upload_to='solutions/photos/%Y/%m/%d/', blank=True, null=True)
    document = models.FileField(upload_to='solutions/docs/%Y/%m/%d/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Решение {self.student} по заданию {self.exercise}"