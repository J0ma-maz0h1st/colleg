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

    def post(self, request, *args, **kwargs):
        task_id = self.kwargs.get('pk')
        task = generics.get_object_or_404(Tasks, pk=task_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(task=task)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ApproveAnswerView(generics.UpdateAPIView):
    queryset = Answers.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsMentorOrAdmin]
    http_method_names = ['patch', 'get']

    def patch(self, request, *args, **kwargs):
        answer = self.get_object()
        answer.is_approved = True
        answer.save()
        return Response({"message": "Ответ одобрен"}, status=status.HTTP_200_OK)
    
    def get(self, request, *args, **kwargs):
        answer = self.get_object()
        serializer = self.get_serializer(answer)
        return Response(serializer.data)

class ListAnswersView(generics.ListAPIView):
    serializer_class = AnswerListSerializer
    permission_classes = [IsMentorOrAdmin]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return Answers.objects.filter(task_id=task_id)
    

    
# class AddQuestionView(generics.CreateAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer
#     permission_classes = [IsMentorOrAdmin]

#     def perform_create(self, serializer):
#         serializer.save()
        

# class QuizSessionView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     # GET: Получаем вопросы
#     def get(self, request, category):
#         questions_query = Question.objects.filter(category=category)
#         if not questions_query.exists():
#             return Response({"error": "Категория не найдена"}, status=404)

#         # Берем 10 случайных
#         questions = list(questions_query.order_by('?')[:10])
        
#         # Перемешиваем варианты ответов в каждом вопросе
#         for q in questions:
#             random.shuffle(q.options)

#         serializer = TakeTestSerializer(questions, many=True)
#         return Response({
#             "questions": serializer.data,
#             "start_time": timezone.now()
#         })


# class SubmitTestResultView(generics.CreateAPIView):
#     """
#     Принимает ответы на тест, сверяет их и сохраняет результат.
#     """
#     queryset = TestResult.objects.all()
#     serializer_class = TestResultCreateSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         # При создании возвращаем созданный объект, чтобы сериализатор 
#         # мог подготовить итоговый ответ (с score, duration и т.д.)
#         return serializer.save()