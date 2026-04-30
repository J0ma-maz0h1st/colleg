from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User, Student, Mentor, Group
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField() # Используем строку, пакет сам провалидирует

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'phone')


    def create(self, validated_data):
        validated_data['role'] = 'student'
        user = User.objects.create_user(**validated_data)
        
        Student.objects.create(user=user)
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        fields = ('old_password', 'new_password',)

class ForgotPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('email',)

class ForgotPasswordConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        fields = ('uid', 'token', 'new_password',)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        fields = ('old_password', 'new_password',)

class ForgotPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('email',)

class ForgotPasswordConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        fields = ('uid', 'token', 'new_password',)


class BaseProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        user = request.user if request else None

        # 1. Если это Хозяин профиля ИЛИ Админ — возвращаем полные данные
        if user and (user == instance.user or user.is_staff):
            return data
            
        # 2. Если это другой пользователь и портфолио СКРЫТО — только обязательные поля
        if not instance.is_portfolio_public:
            mandatory_fields = self.get_mandatory_fields()
            return {key: data[key] for key in mandatory_fields if key in data}
            
        # 3. Если портфолио публичное — возвращаем данные (с учетом Meta exclude)
        return data

    def get_mandatory_fields(self):
        return ['id', 'first_name', 'last_name', 'is_portfolio_public']

# Студент и Ментор наследуют эту логику
class StudentProfileSerializer(BaseProfileSerializer):
    class Meta:
        model = Student
        exclude = ('internal_admin_notes',) # Скрыто даже от владельца (только в БД/Админке)
        read_only_fields = ('potential_points', 'gpa', 'attendance_rate', 'is_frozen')

    def get_mandatory_fields(self):
        return super().get_mandatory_fields() + ['current_education', 'gpa']

class MentorProfileSerializer(BaseProfileSerializer):
    class Meta:
        model = Mentor
        exclude = ('internal_rating',)

    def get_mandatory_fields(self):
        return super().get_mandatory_fields() + ['education_place', 'is_verified']