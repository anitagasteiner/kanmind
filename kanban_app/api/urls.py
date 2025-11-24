from django.urls import path, include
#from rest_framework.routers import DefaultRouter
from .views import BoardsView, BoardDetail, EmailCheckView, TasksView, TaskDetail, TasksAssignedToMeView, TasksReviewingView

# router = DefaultRouter()
# router.register(r'kanban', TaskViewSet, basename='tasks')

urlpatterns = [
    #path('', include(router.urls)),
    path('boards/', BoardsView.as_view(), name='boards-list'),
    path('boards/<int:pk>', BoardDetail.as_view(), name='board-detail'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
    path('tasks/', TasksView.as_view(), name='tasks-list'),
    path('tasks/<int:pk>', TaskDetail.as_view(), name='task-detail'),
    path('tasks/assigned-to-me/', TasksAssignedToMeView.as_view(), name='tasks-assigned-to-me'),
    path('tasks/reviewing', TasksReviewingView.as_view(), name='tasks-reviewing')
]

