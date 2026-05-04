from django.urls import path
from .views import *

urlpatterns = [
    path('list/', CourseViewSet.as_view({'get': 'list'}), name='course-list'),
    path('modules/<int:course_id>/', ModuleViewSet.as_view({'get': 'list'}), name='module-list'),
]