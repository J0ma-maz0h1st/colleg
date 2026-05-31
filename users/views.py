from django.shortcuts import redirect, get_object_or_404
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Student, Mentor, Applications
from .serializers import (
    ChangePasswordSerializer, ForgotPasswordRequestSerializer, ForgotPasswordConfirmSerializer,
    ApplicationCreateSerializer, ApplicationApprovalSerializer,
    StudentProfileSerializer, MentorProfileSerializer
)

User = get_user_model()

# --- КЛАСС ПРАВ ДОСТУПА (PERMISSIONS) ---

class IsOwnerOrAdmin(permissions.BasePermission):
    """Доступ разрешен только владельцу профиля или админу"""
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user


# --- ПРЕДСТАВЛЕНИЯ АВТОРИЗАЦИИ И СБРОСА ПАРОЛЯ ---

class ChangePasswordView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        if not user.check_password(serializer.validated_data.get("old_password")):
            return Response({"error": "Старый пароль неверен"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data.get("new_password"))
        user.save()
        return Response({"message": "Пароль успешно изменен"}, status=status.HTTP_200_OK)


class ForgotPasswordRequestView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ForgotPasswordRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data.get("email")
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Тестовый возврат параметров (в продакшене тут отправка email)
            return Response({
                "message": "Ссылка для сброса сгенерирована",
                "uid": uid,
                "token": token
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Пользователь с таким email не найден"}, status=status.HTTP_404_NOT_FOUND)


class ForgotPasswordConfirmView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ForgotPasswordConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        uid = serializer.validated_data.get("uid")
        token = serializer.validated_data.get("token")
        new_password = serializer.validated_data.get("new_password")

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
            
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({"message": "Пароль успешно сброшен"}, status=status.HTTP_200_OK)
            return Response({"error": "Неверный или просроченный токен"}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Ошибка валидации токена или параметров"}, status=status.HTTP_400_BAD_REQUEST)


# --- ПРЕДСТАВЛЕНИЯ ЗАЯВОК (APPLICATIONS) ---

class ApplicationCreateView(generics.CreateAPIView):
    serializer_class = ApplicationCreateSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        # 1. Проверяем тип запроса. HTML-форма отправляет 'application/x-www-form-urlencoded'
        is_html_form = request.content_type == 'application/x-www-form-urlencoded'

        # 2. Инициализируем и валидируем сериализатор
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            
            # Если запрос пришел с нашего Django-лендинга
            if is_html_form:
                messages.success(request, "Заявка успешно отправлена! Ожидайте подтверждения администратора.")
                return redirect('landing') # Редирект на имя роута '/' (у нас это 'landing')
            
            # Если это был чистый API-запрос (Bruno / Postman / React)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        else:
            # Если валидация провалилась (например, email уже занят или телефон неверный)
            if is_html_form:
                # Собираем все ошибки валидации в красивую строку для юзера
                error_messages = []
                for field, errors in serializer.errors.items():
                    # Переводим технические имена полей на понятный язык для алертов
                    field_name = field
                    if field == 'email': field_name = 'Email'
                    elif field == 'phone': field_name = 'Телефон'
                    elif field == 'first_name': field_name = 'Имя'
                    elif field == 'last_name': field_name = 'Фамилия'
                    
                    error_messages.append(f"{field_name}: {errors[0]}")
                
                full_error_text = "Ошибка заполнения формы! " + " | ".join(error_messages)
                messages.error(request, full_error_text)
                
                # Возвращаем пользователя назад на лендинг к форме, сохраняя фокус на ошибке
                return redirect('/#register-form')
            
            # Для стандартного API возвращаем массив ошибок в формате JSON
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationApprovalView(generics.UpdateAPIView):
    http_method_names = ['patch']
    serializer_class = ApplicationApprovalSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Applications.objects.all()


# --- ПРЕДСТАВЛЕНИЯ ПРОФИЛЕЙ (PROFILES) ---

class BaseProfileView:
    """Общий миксин для динамического определения профиля на основе User ID"""
    def get_object(self):
        # <int:pk> в URL — это ВСЕГДА id модели User
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        if user.role == 'mentor':
            return get_object_or_404(Mentor, user=user)
        return get_object_or_404(Student, user=user)

    def get_serializer_class(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        if user.role == 'mentor':
            return MentorProfileSerializer
        return StudentProfileSerializer


class UserProfileDetailView(BaseProfileView, generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]


class ProfileEditView(BaseProfileView, generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    http_method_names = ['patch']