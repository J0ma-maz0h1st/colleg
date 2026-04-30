from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView # type: ignore

urlpatterns = [
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('password-reset/', ForgotPasswordRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/', ForgotPasswordConfirmView.as_view(), name='password-reset-confirm'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', UserProfileDetailView.as_view()),
    path('profile/<int:pk>/edit/', ProfileEditView.as_view()),
]