from django.urls import path
from .views import *

urlpatterns = [
    path('groups/<int:group_id>/tasks/', TaskListView.as_view(), name='task-list'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    
    path('answers/<int:pk>/', AnswerDetailView.as_view(), name='answer-detail'),
    path('answers/<int:pk>/approve/', ApproveAnswerView.as_view(), name='answer-approve'),
    path('<int:task_id>/answers/', ListAnswersView.as_view(), name='task-answers-list'),
    path('answers/submit/', SubmitAnswerView.as_view(), name='answer-submit'),
    
    # Квизы и тесты
    path('questions/add/', AddQuestionView.as_view(), name='add-question'),
    path('quiz/<str:category>/session/', QuizSessionView.as_view(), name='quiz-session'),
    path('quiz/submit/', SubmitTestResultView.as_view(), name='quiz-submit'),
]