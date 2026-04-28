from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mentor_profile')
    birth_date = models.DateField(verbose_name="Дата рождения")
    department = models.CharField(max_length=100, verbose_name="Кафедра")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    experience_years = models.PositiveIntegerField(default=0, verbose_name="Стаж (лет)")
    qualifications = models.TextField(blank=True, verbose_name="Квалификации")

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    is_active_student = models.BooleanField(default=True)

    def __str__(self):
        return f"Student: {self.user.email}"
    
class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название группы")
    specialty = models.CharField(max_length=100, verbose_name="Специальность")
    mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True, related_name='groups')
    course = models.IntegerField(verbose_name="Курс")
    students = models.ManyToManyField(
        'Student', 
        related_name="groups", 
        blank=True
    )

    def __str__(self):
        return self.name
