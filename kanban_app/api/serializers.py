from rest_framework import serializers
from kanban_app.models import Board, Task


# class TicketSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ticket
#         fields = ['id', 'title', 'board']
#         read_only_fields = ['id']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'due_date']
        read_only_fields = ['id']


class BoardSerializer(serializers.ModelSerializer):
    # tickets = TicketSerializer(many=True, read_only=True)
    # ticket_ids = serializers.PrimaryKeyRelatedField(
    #     queryset=Ticket.objects.all(),
    #     many=True,
    #     write_only=True,
    #     source='tickets'
    # )
    # ticket_count = serializers.SerializerMethodField()

    tasks = TaskSerializer(many=True, read_only=True)
    task_ids = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(),
        many=True,
        write_only=True,
        source='tasks'
    )
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'tasks', 'task_ids', 'ticket_count', 'tasks_to_do_count','tasks_high_prio_count']
        read_only_fields = ['id']

    def get_ticket_count(self, obj):
        return obj.tasks.count()
    
    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status=Task.TO_DO).count()
    
    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority=Task.HIGH).count()


