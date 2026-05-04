from rest_framework import serializers
from .models import Lesson, LessonFile


class LessonFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonFile
        fields = ['id', 'title', 'file']


class LessonSerializer(serializers.ModelSerializer):
    files = LessonFileSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'order', 'description', 'content',
            'video_url', 'video_file', 'duration_minutes',
            'is_preview', 'files'
        ]


class LessonListSerializer(serializers.ModelSerializer):
    """Для списка уроков (без тяжёлого контента)"""
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'order', 'duration_minutes', 'is_preview']