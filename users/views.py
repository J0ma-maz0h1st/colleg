from rest_framework import generics, permissions
from .models import User
from rest_framework import status, permissions
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student, Mentor
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrAdmin # Импортируем наше правило
from .serializers import *

# class RegisterView(generics.CreateAPIView):
#     serializer_class = RegisterSerializer
#     permission_classes = [permissions.AllowAny]


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


class UserProfileDetailView(generics.RetrieveAPIView):
    """Просмотр любого профиля (с логикой маскировки)"""
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)
        return MentorProfileSerializer if user.role == 'mentor' else StudentProfileSerializer

    def get_object(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        if user.role == 'mentor':
            return get_object_or_404(Mentor, user=user)
        return get_object_or_404(Student, user=user)
    


class ProfileEditView(generics.UpdateAPIView):
    """
    Эндпоинт только для частичного редактирования профиля (PATCH).
    Доступно владельцу или админу.
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    # Ограничиваем методы: убираем PUT, оставляем только PATCH
    http_method_names = ['patch'] 

    def get_serializer_class(self):
        # Получаем объект один раз, чтобы определить роль
        obj = self.get_object()
        if obj.user.role == 'mentor':
            return MentorProfileSerializer
        return StudentProfileSerializer

    def get_object(self):
        # Ищем пользователя по pk из URL
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        
        # Возвращаем соответствующий профиль
        if user.role == 'mentor':
            return get_object_or_404(Mentor, user=user)
        return get_object_or_404(Student, user=user)

class ApplicationCreateView(generics.CreateAPIView):
    serializer_class = ApplicationCreateSerializer
    permission_classes = [permissions.AllowAny]

class ApplicationApprovalView(generics.UpdateAPIView):
    http_method_names = ['patch'] # Ограничиваем методы: убираем PUT, оставляем только PATCH
    serializer_class = ApplicationApprovalSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Applications.objects.all()



# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .forms import StudentApplicationForm

# def landing_registration(request):
#     if request.method == 'POST':
#         form = StudentApplicationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Ваша заявка успешно отправлена! Мы свяжемся с вами.')
#             return redirect('registration_success')
#     else:
#         form = StudentApplicationForm()
    
#     return render(request, 'index.html', {'form': form})