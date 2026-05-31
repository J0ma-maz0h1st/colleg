from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.conf import settings
from django.conf.urls.static import static

# Импортируем твои HTML views (предположим, они лежат в back/views.py)
from .views import landing_view, main_dashboard_view, profile_view 

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- API Эндпоинты ---
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api/users/', include('users.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/info/', include('info.urls')),
    path('api/courses/', include('courses.urls')),
    
    # --- HTML Страницы Фронтенда (Django Templates) ---
    path('', landing_view, name='landing'), # Тот самый Лендинг
    path('home/', main_dashboard_view, name='main'), # Главная страница (Каталог, задачи)
    path('profile/<int:pk>/', profile_view, name='profile'), # Личный кабинет
    
    # Временные заглушки для роутов, которые используются в хедере:
    path('login/', landing_view, name='login'), # Пока нет страницы логина, перекинет на лендинг
    path('logout/', landing_view, name='logout'),
    path('courses/', landing_view, name='courses'),
    path('tasks/', landing_view, name='tasks'),
    path('rating/', landing_view, name='rating'),
    path('profile/materials/', landing_view, name='my_materials'),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)