from rest_framework import serializers
from kanban_app.models import Board, Task, Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'board']
        read_only_fields = ['id']


class BoardSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
    ticket_ids = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.all(),
        many=True,
        write_only=True,
        source='tickets'
    )
    ticket_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'ticket_ids', 'ticket_count', 'tickets']
        read_only_fields = ['id']

    def get_ticket_count(self, obj):
        return obj.tickets.count()


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'due_date']
        read_only_fields = ['id']


