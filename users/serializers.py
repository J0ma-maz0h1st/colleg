from rest_framework import serializers
from .models import User, Mentor, Group, Student
from django.contrib.auth import get_user_model

User = get_user_model()

# --- СЕРИАЛИЗАТОР РЕГИСТРАЦИИ ---
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        # Всегда создаем с ролью 'student'
        validated_data['role'] = 'student'
        user = User.objects.create_user(**validated_data)
        
        Student.objects.create(user=user)
        return user

# --- СЕРИАЛИЗАТОР ДЛЯ ЗАПОЛНЕНИЯ ПРОФИЛЯ ---
class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('phone', 'birth_date')

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