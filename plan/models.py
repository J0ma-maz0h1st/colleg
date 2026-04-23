from django.db import models
from users.models import Groups
from users.models import Mentors

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
    time_amount = models.PositiveIntegerField(
    help_text="Общее количество академических часов",
    default=72)
    control_type = models.CharField(max_length=20, choices=ControlType.choices, default=ControlType.EXAM)
    semestr = models.IntegerField(choices=Semester.choices, default=Semester.FIRST)

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

    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    subjects = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentors, on_delete=models.CASCADE, null=True)
    day_of_week = models.CharField(max_length=20, choices=DayOfWeek.choices, default=DayOfWeek.MONDAY)
    lesson_number = models.PositiveIntegerField()
    classroom = models.CharField(max_length=10)
    lesson_type = models.CharField(max_length=15, choices=LessonType.choices, default=LessonType.LECTURE)
    

