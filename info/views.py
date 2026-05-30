from rest_framework import viewsets, permissions
from .models import News, FAQ, AboutSection
from .serializers import NewsSerializer, FAQSerializer, AboutSectionSerializer

class ReadOnlyOrAdminPermission(permissions.BasePermission):
    """Кастомное правило: читать могут все, менять — только персонал/админы."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return bool(request.user and request.user.is_staff)


class NewsViewSet(viewsets.ModelViewSet):
    """Эндпоинт для работы с новостями."""
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [ReadOnlyOrAdminPermission]

    def get_authentication_classes(self):
        # Если это простой просмотр — отключаем обязательный JWT проверку
        if self.request.method in permissions.SAFE_METHODS:
            return []
        return super().get_authentication_classes()


class FAQViewSet(viewsets.ModelViewSet):
    """Эндпоинт для работы с разделом FAQ."""
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [ReadOnlyOrAdminPermission]

    def get_authentication_classes(self):
        if self.request.method in permissions.SAFE_METHODS:
            return []
        return super().get_authentication_classes()


class AboutSectionViewSet(viewsets.ModelViewSet):
    """Эндпоинт для управления контентом страницы 'О нас'."""
    queryset = AboutSection.objects.all()
    serializer_class = AboutSectionSerializer
    permission_classes = [ReadOnlyOrAdminPermission]

    def get_authentication_classes(self):
        if self.request.method in permissions.SAFE_METHODS:
            return []
        return super().get_authentication_classes()

#статистика с количеством студентов(за все время и текущее), курсов, направлений, менторов, количество компаний с которыми сотрудничаем, количество открытых вакансий, количество закрытых вакансий, количество активных групп, количество завершенных групп.

class StatisticsViewSet(viewsets.ViewSet):
    """Эндпоинт для получения статистики по платформе."""
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        from users.models import Student, Mentor, Group
        from courses.models import Course, Direction
        
        data = {
            "total_students": Student.objects.count(),
            "current_students": Student.objects.filter(user__is_active=True).count(),
            "total_mentors": Mentor.objects.count(),
            "total_courses": Course.objects.count(),
            "total_directions": Direction.objects.count(),
            "active_groups": Group.objects.filter(is_active=True).count(),
            "completed_groups": Group.objects.filter(is_active=False).count(),
            # Дополнительно можно добавить компании и вакансии, если есть соответствующие модели
        }
        return Response(data)

