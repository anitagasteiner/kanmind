from rest_framework import generics
from rest_framework.response import Response
from kanban_app.models import Task
from .serializers import TaskSerializer
from kanban_app.models import Task

class TasksView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    # def get_queryset(self):
    #     return self.request.tasks.all()

    # def perform_create(self, serializer):
    #     serializer.save()



    # def get(self, request):
    #     tasks = Task.objects.all()
    #     serializer = TaskSerializer(tasks, many=True)
    #     return Response(serializer.data)
    
