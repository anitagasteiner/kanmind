from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from .views import TasksView

# router = DefaultRouter()
# router.register(r'achievements', AchievementViewSet, basename='achievement')

urlpatterns = [
    # path('', include(router.urls)),
    path('tasks/', TasksView.as_view(), name='api-test'),
]

