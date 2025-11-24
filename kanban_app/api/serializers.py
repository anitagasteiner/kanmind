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


class UserMiniSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return obj.get_full_name()


class TaskCreateSerializer(serializers.ModelSerializer):
    #assignee_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
        write_only=True
    )
    assignee = UserMiniSerializer(read_only=True)
    reviewer = UserMiniSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES)
    priority = serializers.ChoiceField(choices=Task.PRIORITY_CHOICES)

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority', 'assignee_id', 'reviewer_id', 'assignee', 'reviewer', 'due_date', 'comments_count']

    def get_comments_count(self, obj):
        return 0 # TODO Comments sind noch nicht implementiert!
    
    def create(self, validated_data):
        assignee = validated_data.pop('assignee_id')
        reviewer = validated_data.pop('reviewer_id', None)

        # try:
        #     assignee = User.objects.get(id=assignee_id)
        # except User.DoesNotExist:
        #     raise serializers.ValidationError({'assignee_id': 'User does not exist.'})

        # reviewer = None
        # if reviewer_id is not None:
        #     try:
        #         reviewer = User.objects.get(id=reviewer_id)
        #     except User.DoesNotExist:
        #         raise serializers.ValidationError({'reviewer_id': 'User does not exist.'})
            
        task = Task.objects.create(
            assignee=assignee,
            reviewer=reviewer,
            **validated_data
        )
        #task.assignee.set([assignee])

        return task


class TaskAssignedSerializer(serializers.ModelSerializer):
    assignee = serializers.SerializerMethodField()
    reviewer = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'board', 'title','description', 'status', 'priority', 'assignee', 'reviewer', 'due_date', 'comments_count']

    def get_assignee(self, obj):
        user = obj.assignee.first()
        if not user:
            return None
        return UserMiniSerializer(user).data
    
    def get_reviewer(self, obj):
        return None # TODO: Reviewer ist noch nicht implementiert!
    
    def get_comments_count(self, obj):
        return 0 # TODO Comments existieren noch nicht!
    