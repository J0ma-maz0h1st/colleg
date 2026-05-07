from .models import Tasks, Answers
from rest_framework import serializers


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id', 'title', 'description', 'group', 'created_at', 'updated_at', 'file', 'photo']


class TaskListSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Tasks
        fields = ['id', 'title', 'description', 'group', 'created_at', 'updated_at']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ['id', 'task', 'student', 'content', 'submitted_at', 'is_approved', 'file', 'photo']
    
class AnswerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ['id', 'task', 'student', 'content', 'submitted_at', 'is_approved']