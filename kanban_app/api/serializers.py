from rest_framework import serializers
from kanban_app.models import Board, Task


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title']
        read_only_fields = ['id']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'due_date']
        read_only_fields = ['id']

