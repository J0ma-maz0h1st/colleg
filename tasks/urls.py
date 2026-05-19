from django.urls import path
from .views import *

urlpatterns = [
    path('<int:group_id>/list/', TaskListView.as_view(), name='task-list'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('answers/submit/', SubmitAnswerView.as_view(), name='submit-answer'),
    path('answers/<int:task_id>/', ListAnswersView.as_view(), name='list-answers'),
    path('answers/<int:pk>/', AnswerDetailView.as_view(), name='answer-detail'),
    path('answers/<int:pk>/approve/', ApproveAnswerView.as_view(), name='answer-approve'),


    # path('question/<str:category>/', QuizSessionView.as_view(), name='quiz-session'),
    # path('test/result/', SubmitTestResultView.as_view(), name='test-result'),
    # path('question/add/', AddQuestionView.as_view(), name='add-question'),
]