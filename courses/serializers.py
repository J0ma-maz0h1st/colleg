#сериализаторы
from rest_framework import serializers
from .models import Course, Direction

class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'photo']

class CourseSerializer(serializers.ModelSerializer):
    direction = DirectionSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'cost', 'max_students_count', 'current_students_count', 'direction', 'type', 'level', 'photo', 'created_at', 'updated_at']
