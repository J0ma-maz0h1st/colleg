from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Module, Enrollment
from .serializers import (
    CourseListSerializer, CourseDetailSerializer,
    ModuleSerializer, EnrollmentSerializer
)
from users.permissions import IsOwnerOrAdmin


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.prefetch_related('modules').select_related('mentor')
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        course = self.get_object()
        student = request.user

        if student.role != 'student':
            return Response({"error": "Только студенты могут записываться"}, status=400)

        enrollment, created = Enrollment.objects.get_or_create(
            student=student, course=course
        )
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ModuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]