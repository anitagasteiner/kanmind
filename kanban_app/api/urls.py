"""
URL routes for the Kanmind API.

This module maps HTTP endpoints to their corresponding view classes.  
It organizes routes for boards, tasks, user-specific task filters, and task comments.
"""

from django.urls import path
from .views import BoardsView, BoardDetail, EmailCheckView, TasksView, TaskDetail, TasksAssignedToMeView, TasksReviewingView, CommentsView, CommentDetail

urlpatterns = [
    path('boards/', BoardsView.as_view(), name='boards-list'),
    path('boards/<int:pk>', BoardDetail.as_view(), name='board-detail'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
    path('tasks/', TasksView.as_view(), name='tasks-list'),
    path('tasks/<int:pk>', TaskDetail.as_view(), name='task-detail'),
    path('tasks/assigned-to-me/', TasksAssignedToMeView.as_view(), name='tasks-assigned-to-me'),
    path('tasks/reviewing', TasksReviewingView.as_view(), name='tasks-reviewing'),
    path('tasks/<int:pk>/comments/', CommentsView.as_view(), name='comments-list'),
    path('tasks/<int:task_pk>/comments/<int:pk>', CommentDetail.as_view(), name='comment-detail')
]

