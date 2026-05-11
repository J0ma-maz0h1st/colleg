from django.urls import path
from .views import *

urlpatterns = [
    path('<int:group_id>/list/', TaskListView.as_view(), name='task-list'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('<int:pk>/submit/', SubmitAnswerView.as_view(), name='submit-answer'),
    path('<int:pk>/approve/', ApproveAnswerView.as_view(), name='approve-answer'),
    path('<int:task_id>/answers/', ListAnswersView.as_view(), name='list-answers'),


    # path('quiz/', GetQuizView.as_view(), name='get-quiz'),
    # path('quiz/submit/', SubmitQuizView.as_view(), name='submit-quiz'),
    path('question/add/', AddQuestionView.as_view(), name='add-question'),
]