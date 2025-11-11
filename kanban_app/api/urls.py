from django.urls import path, include
#from rest_framework.routers import DefaultRouter
from .views import TasksView, TaskDetail

# router = DefaultRouter()
# router.register(r'kanban', TaskViewSet, basename='tasks')

urlpatterns = [
    #path('tasks/', include(router.urls)),
    path('tasks/', TasksView.as_view(), name='tasks-list'),
    path('tasks/<int:pk>', TaskDetail.as_view(), name='task-detail')
]

