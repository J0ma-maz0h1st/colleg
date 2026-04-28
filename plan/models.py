from django.db import models
from users.models import Group
from users.models import Mentor

# Create your models here.
class Subjects(models.Model):
    class ControlType(models.TextChoices):
        EXAM = 'EXAM', 'Экзамен'
        CREDIT = 'CREDIT', 'Зачет'
        PROJECT = 'PROJECT', 'Курсовая работа'

    class Semester(models.IntegerChoices):
        FIRST = 1, '1 семестр'
        SECOND = 2, '2 семестр'
        THIRD = 3, '3 семестр'
        FOURTH = 4, '4 семестр'
        FIFTH = 5, '5 семестр'
        SIXTH = 6, '6 семестр'
        SEVENTH = 7, '7 семестр'
        EIGHTH = 8, '8 семестр'

    subjects_name = models.CharField(max_length=35, verbose_name="Название предмета")
    time_amount = models.PositiveIntegerField(help_text="Общее количество часов", default=72, verbose_name="Часы")
    control_type = models.CharField(max_length=20, choices=ControlType.choices, default=ControlType.EXAM, verbose_name="Тип контроля")
    semestr = models.IntegerField(choices=Semester.choices, default=Semester.FIRST, verbose_name="Семестр")

class Schedule(models.Model):
    class LessonType(models.TextChoices):
        LECTURE = 'LECTURE', 'Лекция'
        PRACTICE = 'PRACTICE', 'Практика'
        LAB = 'LAB', 'Лабораторная'
    
    class DayOfWeek(models.IntegerChoices):
        MONDAY = 1, 'Понедельник'
        TUESDAY = 2, 'Вторник'
        WEDNESDAY = 3, 'Среда'
        THURSDAY = 4, 'Четверг'
        FRIDAY = 5, 'Пятница'
        SATURDAY = 6, 'Суббота'

    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа") 
    subjects = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name="Предмет")
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, null=True, verbose_name="Преподователь")
    day_of_week = models.CharField(max_length=20, choices=DayOfWeek.choices, default=DayOfWeek.MONDAY, verbose_name="День недели")
    lesson_number = models.PositiveIntegerField(verbose_name="Номер пары")
    classroom = models.CharField(max_length=10, verbose_name="Аудитория")
    lesson_type = models.CharField(max_length=15, choices=LessonType.choices, default=LessonType.LECTURE, verbose_name="Тип занятия")
    