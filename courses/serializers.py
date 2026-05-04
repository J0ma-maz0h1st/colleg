from rest_framework import serializers
from .models import Course, Module, Enrollment
from users.serializers import StudentProfileSerializer  # если нужно


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'title', 'order', 'description']


class CourseListSerializer(serializers.ModelSerializer):
    mentor_name = serializers.CharField(source='mentor.get_full_name', read_only=True)
    enrolled_count = serializers.IntegerField(source='students_enrolled', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'short_description', 'thumbnail',
            'price', 'level', 'duration_hours', 'direction',
            'mentor_name', 'enrolled_count', 'is_published'
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    mentor_name = serializers.CharField(source='mentor.get_full_name', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'short_description',
            'thumbnail', 'price', 'level', 'duration_hours', 'direction',
            'mentor', 'mentor_name', 'modules', 'is_published', 'created_at'
        ]


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'enrolled_at', 'is_completed', 'completed_at']
        read_only_fields = ['student']