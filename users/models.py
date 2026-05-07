from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField # type: ignore
from phonenumber_field.widgets import PhoneNumberPrefixWidget # type: ignore

# --- МЕНЕДЖЕР ПОЛЬЗОВАТЕЛЕЙ ---
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# --- КАСТОМНЫЙ ПОЛЬЗОВАТЕЛЬ ---
class User(AbstractBaseUser, PermissionsMixin):
    """
    Модель пользователя системы.
    Расширяет AbstractBaseUser и PermissionsMixin для кастомной аутентификации
    с email в качестве поля имени пользователя. Включает поля для личной информации,
    роли и деталей регистрации.
    """
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    role = models.CharField(max_length=20, choices=[
        ('student', 'Студент'),
        ('mentor', 'Преподаватель'),
        ('admin', 'Администратор'),
    ], verbose_name="Роль")
    phone = PhoneNumberField(verbose_name="Телефон", unique=True, region='KG')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class Mentor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mentor_profile', limit_choices_to={'role': 'mentor'},)
    
    # Редактируемые данные (Публичные)
    avatar = models.ImageField(upload_to='mentors/avatars/', null=True, blank=True)
    bio = models.TextField(verbose_name="Биография", blank=True)
    work_history = models.TextField(verbose_name="Опыт работы", blank=True, default="Не указано")
    education_place = models.CharField(max_length=255, verbose_name="Учебное заведение")
    qualifications = models.TextField(verbose_name="Квалификации/Сертификаты")
    skills = models.CharField(max_length=255, verbose_name="Навыки (через запятую)", blank=True, default="Не указано")
    video_presentation = models.URLField(blank=True, null=True, verbose_name="Ссылка на видео-визитку")
    
    # Социальные ссылки
    whatsapp = models.CharField(max_length=20, blank=True, null=True, verbose_name="WhatsApp")
    github = models.URLField(blank=True, verbose_name="GitHub")
    
    # Системные данные (Только для Админа/Автоматики)
    is_verified = models.BooleanField(default=False, verbose_name="Проверен администрацией")
    internal_rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    total_students_taught = models.PositiveIntegerField(default=0)
    experience_start_date = models.DateField(auto_now_add=True, verbose_name="Дата начала работы в школе")
    is_portfolio_public = models.BooleanField(default=False, verbose_name="Сделать портфолио публичным")
    
    # Статус профиля
    is_frozen = models.BooleanField(default=False, verbose_name="Заморожен")

    class Meta:
        verbose_name = "Профиль Ментора"
        verbose_name_plural = "Профили Менторов"


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile', limit_choices_to={'role': 'student'},)
    study_goal = models.TextField(verbose_name="Цель обучения", help_text="Что хочет освоить?", blank=True, default="Не указано")
    current_education = models.CharField(max_length=255, verbose_name="Место текущего обучения")
    is_portfolio_public = models.BooleanField(default=False, verbose_name="Сделать портфолио публичным")
    portfolio_links = models.JSONField(default=list, blank=True, help_text="Список ссылок на проекты")
    gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    attendance_rate = models.PositiveIntegerField(default=0) # В %
    
    # --- ОЧКИ ПОТЕНЦИАЛА ---
    # Это поле будет пересчитываться сложным алгоритмом
    potential_points = models.IntegerField(default=0, verbose_name="Очки потенциала")
    
    total_speed_score = models.FloatField(default=0.0, verbose_name="Среднее кол-во попыток")
    total_attempts = models.PositiveIntegerField(default=0, verbose_name="Коэффициент скорости решения")
    total_recommendations = models.PositiveIntegerField(default=0)
    
    
    
    parent_contact = models.CharField(max_length=255, blank=True, null=True, verbose_name="Контакт родителя")
    is_parent_contact_approved = models.BooleanField(default=False)
    is_frozen = models.BooleanField(default=False)
    internal_admin_notes = models.TextField(blank=True, verbose_name="Заметки для администрации", null=True)
    


    def update_potential_points(self, weights=None):
        """Расчёт по твоей формуле"""
        if weights is None:
            weights = {'w1': 0.4, 'w2': 0.35, 'w3': 0.25}  # настраиваемые

        if self.total_attempts == 0:
            self.potential_points = 0
            self.save()
            return

        S = self.total_speed_score
        A = max(self.total_attempts, 1)
        R = self.total_recommendations

        P = (S * weights['w1']) + ((1 / A) * weights['w2']) + (R * weights['w3'])
        self.potential_points = int(P * 100)  # масштабируем до удобных чисел
        self.save()

        
    class Meta:
        verbose_name = "Профиль Студента"
        verbose_name_plural = "Профили Студентов"

class Group(models.Model):
    class Direction(models.TextChoices):
        OOP = 'OOP', 'ООП'
        Python = 'Python', 'Python'
        Cpp = 'C++', 'C++'
        SysProg = 'SysProg', 'Системное программирование'
        WebProg = 'WebProg', 'Web-программирование'
        JS = 'JS', 'JavaScript'
        Algorithms = 'Algorithms', 'Алгоритмы'
        DataStructer = 'DataStructer', 'Структуры данных'

    name = models.CharField(max_length=100, verbose_name="Название группы")
    direction = models.CharField(choices=Direction.choices, max_length=100, verbose_name="Направление (напр. Python)")
    min_skill_level = models.IntegerField(default=1)
    max_capacity = models.PositiveIntegerField(default=15)
    course = models.IntegerField(default=1)

    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                               null=True, blank=True,
                               limit_choices_to={'role': 'mentor'},
                               related_name='mentored_groups')

    students = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      limit_choices_to={'role': 'student'},
                                      related_name='learning_groups',
                                      blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"




class Applications(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'В ожидании'
        ACCEPTED = 'ACCEPTED', 'Принято'
        REJECTED = 'REJECTED', 'Отклонено'

    status = models.CharField(choices=Status.choices, max_length=20, default=Status.PENDING)
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    phone = PhoneNumberField(verbose_name="Телефон", unique=True, region='KG')
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=128, verbose_name="Пароль")

    class Meta:
        verbose_name = "Заявка на регистрацию"
        verbose_name_plural = "Заявки на регистрацию"