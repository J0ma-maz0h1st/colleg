from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Course, Direction
from .serializers import CourseSerializer, DirectionSerializer

#нужно сделать так чтобы было 2 эндпоинта для курсов: 1. Получение всех курсов, 2. Получение курса по id для детального просмотра. И 1 эндпоинт для получения всех направлений.

class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]

class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]

class DirectionListView(generics.ListAPIView):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer
    permission_classes = [permissions.AllowAny]