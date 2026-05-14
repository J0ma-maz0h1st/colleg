from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User, Student, Mentor, Group, Applications
User = get_user_model()


# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     phone = serializers.CharField(required=True)
    

#     class Meta:
#         model = User
#         fields = ('email', 'first_name', 'last_name', 'password', 'phone')


#     def create(self, validated_data):
#         if User.objects.filter(phone=validated_data['phone']).exists():
#             raise serializers.ValidationError("Пользователь с таким номером телефона уже существует.")
#         validated_data['role'] = 'student'
#         user = User.objects.create_user(**validated_data)
        
#         Student.objects.create(user=user)
#         return user

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
        # Проверяем, изменился ли статус на "одобренный"
        if validated_data.get('status') == 'ACCEPTED' and instance.status != 'ACCEPTED':
            # Проверяем, не существует ли уже пользователь с таким email
            if not User.objects.filter(email=instance.email).exists():
                # Создаем пользователя с данными из заявки
                if User.objects.filter(phone=instance.phone).exists():
                    raise serializers.ValidationError("Пользователь с таким номером телефона уже существует.")
                validated_data['role'] = 'student'
                user = User.objects.create_user(
                    email=instance.email,
                    first_name=instance.first_name,
                    role='student',
                    last_name=instance.last_name,
                    phone=instance.phone,
                    password=instance.password
                )
                # Создаем профиль студента
                Student.objects.create(user=user)
        
        # Обновляем статус заявки
        instance.status = validated_data['status']
        instance.save()
        return instance

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