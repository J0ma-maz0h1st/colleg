from django.db import models

class Direction(models.Model):
    name = models.CharField(max_length=255, verbose_name="Направление")
    description = models.TextField(verbose_name="Описание направления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    photo = models.ImageField(upload_to='directions/photos/', null=True, blank=True, verbose_name="Фото направления")

    class Meta:
        verbose_name = "Направление"
        verbose_name_plural = "Направления"

class Course(models.Model):
    class CourseType(models.TextChoices):
        ONLINE = 'Online', 'Онлайн'
        OFFLINE = 'Offline', 'Оффлайн'
        HYBRID = 'Hybrid', 'Гибридный'
    class CourseLevel(models.TextChoices):
        BEGINNER = 'Beginner', 'Начальный'
        INTERMEDIATE = 'Intermediate', 'Средний'
        ADVANCED = 'Advanced', 'Продвинутый'
    name = models.CharField(max_length=255, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание курса")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость курса")
    max_students_count = models.IntegerField(verbose_name="Макс. количество студентов", default=12)
    current_students_count = models.IntegerField(verbose_name="Текущее количество студентов", default=0)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name='courses', verbose_name="Направление", null=True, blank=True)
    type = models.CharField(max_length=20, choices=CourseType.choices, verbose_name="Тип курса")
    level = models.CharField(max_length=20, choices=CourseLevel.choices, verbose_name="Уровень сложности")
    photo = models.ImageField(upload_to='courses/photos/', null=True, blank=True, verbose_name="Фото курса")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


