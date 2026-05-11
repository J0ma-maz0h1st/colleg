from django.shortcuts import render
from .serializers import *
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Tasks, Answers, Question, TestResult
from .permissions import IsMentorOrAdmin
from rest_framework.views import APIView
import random
from django.utils import timezone



class TaskListView(generics.ListAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        return Tasks.objects.filter(group_id=group_id)


class TaskDetailView(generics.RetrieveAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaskCreateView(generics.CreateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [IsMentorOrAdmin]

class SubmitAnswerView(generics.CreateAPIView):
    queryset = Answers.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class ApproveAnswerView(generics.UpdateAPIView):
    queryset = Answers.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsMentorOrAdmin]

    def patch(self, request, *args, **kwargs):
        answer = self.get_object()
        answer.is_approved = True
        answer.save()
        return Response({"message": "Ответ одобрен"}, status=status.HTTP_200_OK)

class ListAnswersView(generics.ListAPIView):
    serializer_class = AnswerListSerializer
    permission_classes = [IsMentorOrAdmin]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return Answers.objects.filter(task_id=task_id)
    

    
class AddQuestionView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsMentorOrAdmin]

    def perform_create(self, serializer):
        serializer.save()
        