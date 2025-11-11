from rest_framework import serializers
from kanban_app.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description']
        read_only_fields = ['id']