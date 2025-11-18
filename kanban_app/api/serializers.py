from rest_framework import serializers
from django.contrib.auth.models import User
from kanban_app.models import Board, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'due_date']
        read_only_fields = ['id']


class BoardSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=False
    )
    member_count = serializers.SerializerMethodField()
    # tasks = TaskSerializer(many=True, read_only=True)
    # task_ids = serializers.PrimaryKeyRelatedField(
    #     queryset=Task.objects.all(),
    #     many=True,
    #     write_only=True,
    #     source='tasks'
    # )
    tasks_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'member_count', 'tasks_count', 'tasks_to_do_count','tasks_high_prio_count', 'owner_id']
        read_only_fields = ['id']

    def get_member_count(self, obj):
        return obj.members.count()

    def get_tasks_count(self, obj):
        return obj.tasks.count()
    
    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to_do').count()
    
    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()
    
    def create(self, validated_data):
        members = validated_data.pop('members', [])
        owner = self.context['request'].user # Owner aus context (request.user); Owner ist immer der eingeloggte User.
        board = Board.objects.create(owner=owner, **validated_data)
        board.members.set(members)
        return board


class BoardDetailSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True
    )
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']
        read_only_fields = ['id']


class BoardUpdateSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=Board.members.field.related_model.objects.all(), # User.objects
        many=True
    )

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner', 'members']


