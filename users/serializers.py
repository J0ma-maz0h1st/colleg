from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student, Mentor, Applications

User = get_user_model()

# --- СЕРИАЛИЗАТОРЫ АВТОРИЗАЦИИ И СБРОСА ПАРОЛЯ ---

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

class ForgotPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ForgotPasswordConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, write_only=True)


# --- СЕРИАЛИЗАТОРЫ ЗАЯВОК (APPLICATIONS) ---

class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applications
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

class ApplicationApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applications
        fields = ('id', 'status')

    def update(self, instance, validated_data):
        if validated_data.get('status') == 'ACCEPTED' and instance.status != 'ACCEPTED':
            if User.objects.filter(email=instance.email).exists():
                raise serializers.ValidationError({"email": "Пользователь с таким email уже существует."})
            if User.objects.filter(phone=instance.phone).exists():
                raise serializers.ValidationError({"phone": "Пользователь с таким номером телефона уже существует."})
            
            # Создаем системного пользователя
            user = User.objects.create_user(
                email=instance.email,
                first_name=instance.first_name,
                last_name=instance.last_name,
                phone=instance.phone,
                password=instance.password,
                role='student'
            )
            # Привязываем профиль студента
            Student.objects.get_or_create(user=user)
        
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


# --- СЕРИАЛИЗАТОРЫ ПРОФИЛЕЙ С МАСКИРОВКОЙ ДАННЫХ ---

class BaseProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        user = request.user if request else None

        # 1. Если это Хозяин профиля ИЛИ Администратор — отдаем всё
        if user and (user == instance.user or user.is_staff):
            return data
            
        # 2. Если портфолио скрыто от посторонних — отдаем только публичный минимум
        if not getattr(instance, 'is_portfolio_public', True):
            mandatory_fields = self.get_mandatory_fields()
            return {key: data[key] for key in mandatory_fields if key in data}
            
        return data

    def get_mandatory_fields(self):
        return ['id', 'first_name', 'last_name', 'is_portfolio_public']


class StudentProfileSerializer(BaseProfileSerializer):
    class Meta:
        model = Student
        exclude = ('internal_admin_notes',) 
        read_only_fields = ('potential_points', 'gpa', 'attendance_rate', 'is_frozen')

    def get_mandatory_fields(self):
        # Добавляем специфичные поля для маскировки студента
        return super().get_mandatory_fields() + ['current_education', 'gpa']


class MentorProfileSerializer(BaseProfileSerializer):
    class Meta:
        model = Mentor
        fields = '__all__'

    def get_mandatory_fields(self):
        return super().get_mandatory_fields() + ['bio', 'specialization']