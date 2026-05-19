from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ChangePasswordView, ForgotPasswordRequestView, ForgotPasswordConfirmView,
    ApplicationCreateView, ApplicationApprovalView,
    UserProfileDetailView, ProfileEditView
)

urlpatterns = [
    # JWT авторизация
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Безопасность и пароли
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('password-reset/', ForgotPasswordRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/', ForgotPasswordConfirmView.as_view(), name='password-reset-confirm'),
    
    # Заявки (Анкетирование на входе)
    path('application/create/', ApplicationCreateView.as_view(), name='application-create'),
    path('application/<int:pk>/approve/', ApplicationApprovalView.as_view(), name='application-approve'),
    
    # Профили (Универсальные эндпоинты по User ID)
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='user-profile-detail'),
    path('profile/<int:pk>/edit/', ProfileEditView.as_view(), name='user-profile-edit'),
]