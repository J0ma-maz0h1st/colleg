import random
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tasks, Answers, Question, TestResult
from .permissions import IsMentorOrAdmin, IsStudent  # Добавили IsStudent
from .serializers import (
    TaskListSerializer,
    TasksSerializer,
    AnswerDetailSerializer,
    AnswerListSerializer,
    AnswerSerializer,
    QuestionSerializer,
    TakeTestSerializer,
    TestResultCreateSerializer
)


class TaskListView(generics.ListAPIView):
    """Получение списка задач для конкретной группы."""
    serializer_class = TaskListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        return Tasks.objects.filter(group_id=group_id)


class TaskDetailView(generics.RetrieveAPIView):
    """Детальный просмотр задачи."""
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaskCreateView(generics.CreateAPIView):
    """Создание задачи (доступно Менторам и Админам)."""
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [IsMentorOrAdmin]


class AnswerDetailView(generics.RetrieveAPIView):
    """Просмотр деталей ответа студента."""
    queryset = Answers.objects.all()
    serializer_class = AnswerDetailSerializer
    permission_classes = [IsMentorOrAdmin]

    def get_object(self):
        answer_id = self.kwargs.get('pk')
        return get_object_or_404(Answers, id=answer_id)


class ApproveAnswerView(generics.GenericAPIView):
    """Одобрение ответа ментором."""
    queryset = Answers.objects.all()
    permission_classes = [IsMentorOrAdmin]
    serializer_class = AnswerDetailSerializer

    def post(self, request, *args, **kwargs):
        answer = self.get_object()
        
        if answer.is_approved:
            return Response({"message": "Ответ уже был одобрен ранее"}, status=status.HTTP_400_BAD_REQUEST)
            
        answer.is_approved = True
        answer.save()
        
        return Response({"message": "Ответ успешно одобрен"}, status=status.HTTP_200_OK)
    

class ListAnswersView(generics.ListAPIView):
    """Список всех ответов на конкретную задачу."""
    serializer_class = AnswerListSerializer
    permission_classes = [IsMentorOrAdmin]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return Answers.objects.filter(task_id=task_id)


class SubmitAnswerView(generics.CreateAPIView):
    """Отправка или обновление ответа (только для Студентов)."""
    queryset = Answers.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent] # Заменили ручную проверку на пермишен

    def post(self, request, *args, **kwargs):
        task_id = request.data.get('task')
        existing_answer = Answers.objects.filter(student=request.user, task_id=task_id).first()
        
        if existing_answer:
            if existing_answer.is_approved:
                return Response(
                    {"error": "Задача уже одобрена. Вы не можете изменить ответ."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = self.get_serializer(existing_answer, data=request.data, partial=True)
            message = "Ответ успешно обновлен"
            status_code = status.HTTP_200_OK
        else:
            serializer = self.get_serializer(data=request.data)
            message = "Ответ успешно создан"
            status_code = status.HTTP_201_CREATED

        serializer.is_valid(raise_exception=True)
        serializer.save(student=request.user)

        return Response({
            "message": message,
            "data": serializer.data
        }, status=status_code)


class AddQuestionView(generics.CreateAPIView):
    """Добавление вопросов в пул тестов."""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsMentorOrAdmin]


class QuizSessionView(APIView):
    """Получение 10 случайных вопросов по выбранной категории."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, category):
        questions_query = Question.objects.filter(category=category)
        if not questions_query.exists():
            return Response({"error": "Категория не найдена"}, status=status.HTTP_404_NOT_FOUND)

        # Выбираем до 10 случайных вопросов
        questions = list(questions_query.order_by('?')[:10])
        
        # Безопасно перемешиваем варианты ответов (не трогая оригинал в БД)
        for q in questions:
            shuffled_options = list(q.options)
            random.shuffle(shuffled_options)
            q.options = shuffled_options

        serializer = TakeTestSerializer(questions, many=True)
        return Response({
            "questions": serializer.data,
            "start_time": timezone.now()
        }, status=status.HTTP_200_OK)


class SubmitTestResultView(generics.CreateAPIView):
    """Прием ответов на тест, автоматическая сверка результатов и сохранение."""
    queryset = TestResult.objects.all()
    serializer_class = TestResultCreateSerializer
    permission_classes = [permissions.IsAuthenticated]