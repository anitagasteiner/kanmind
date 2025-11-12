from rest_framework import generics
#from rest_framework.viewsets import ModelViewSet
#from rest_framework.response import Response
#from django.shortcuts import get_object_or_404
from kanban_app.models import Board, Task
from .serializers import BoardSerializer, TaskSerializer


class BoardsView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class TasksView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
# class TaskViewSet(ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer


