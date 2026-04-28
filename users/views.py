from rest_framework import generics, permissions
from .models import User
from .serializers import RegisterSerializer, StudentProfileUpdateSerializer, ChangePasswordSerializer, ForgotPasswordRequestSerializer, ForgotPasswordConfirmSerializer
from rest_framework import status, permissions
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# Дозаполнение профиля студента
class UpdateMyProfileView(generics.UpdateAPIView):
    serializer_class = StudentProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Возвращаем профиль именно того, кто делает запрос
        return Student.objects.get(user=self.request.user)
    

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"error": "Старый пароль неверен"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Пароль успешно изменен"}, status=status.HTTP_200_OK)

class ForgotPasswordRequestView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ForgotPasswordRequestSerializer

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # В реальном проекте здесь отправляется Email. 
            # Сейчас просто вернем это в ответе для теста:
            return Response({
                "message": "Ссылка для сброса сгенерирована",
                "uid": uid,
                "token": token
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)


class ForgotPasswordConfirmView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ForgotPasswordConfirmSerializer

    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        try:
            id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=id)
            
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({"message": "Пароль успешно сброшен"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Неверный или просроченный токен"}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Ошибка валидации"}, status=status.HTTP_400_BAD_REQUEST)