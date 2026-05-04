from django.urls import path
from .views import *

urlpatterns = [
    path('list/', LessonViewSet.as_view({'get': 'list'}), name='lesson-list'),
    path('<int:pk>/', LessonViewSet.as_view({'get': 'retrieve'}), name='lesson-detail'),
]