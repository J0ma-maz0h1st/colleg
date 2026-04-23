from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email — обязательное поле')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
  

class Mentors(models.Model):
    class DepartmentChoices(models.TextChoices):
        IT = 'IT', 'Information Technology'
        DESIGN = 'DESIGN', 'Design'
        ECONOMICS = 'ECONOMICS', 'Economics'
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Пользователи")
    birth_date = models.DateField()
    department = models.CharField(max_length=50, choices=DepartmentChoices.choices, default=DepartmentChoices.IT)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"Mentor: {self.user.get_full_name() or self.user.email}"

class Groups(models.Model):
    group_name = models.CharField(max_length=20)
    specialty = models.CharField(max_length=100)
    course = models.IntegerField()
    mentor = models.ForeignKey(Mentors, on_delete=models.CASCADE, related_name="Ментор")

    def __str__(self):
        return self.group_name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Пользователь")
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name="Группы")
    birth_date = models.DateField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"Student: {self.user.get_full_name() or self.user.email}"
    

    

