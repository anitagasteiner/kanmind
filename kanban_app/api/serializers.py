from rest_framework import serializers
from django.contrib.auth.models import User
from kanban_app.models import Board, Task, Comment


class TaskSerializer(serializers.ModelSerializer):
    #     members = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(),
    #     many=True,
    #     required=False
    # )

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


class UserMiniSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return obj.get_full_name()


class BoardDetailSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(
        source='owner.id',
        read_only=True
    )
    members = serializers.SerializerMethodField()
    tasks = TaskSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']
        read_only_fields = ['id', 'title', 'owner_id', 'members', 'tasks']

    def get_members(self, obj):
        return UserMiniSerializer(obj.members.all(), many=True).data


class BoardUpdateSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=Board.members.field.related_model.objects.all(), # User.objects
        many=True,
        write_only=True
    )
    owner_data = UserMiniSerializer(
        source='owner',
        read_only=True
    )
    members_data = UserMiniSerializer(
        source='members',
        many=True,
        read_only=True
    )

    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'owner_data', 'members_data']
        read_only_fields = ['id', 'owner_data', 'members_data']


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
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
            
        task = Task.objects.create(
            assignee=assignee,
            reviewer=reviewer,
            **validated_data
        )

        return task
    
    def update(self, instance, validated_data):
        if 'assignee_id' in validated_data:
            instance.assignee = validated_data.pop('assignee_id')

        if 'reviewer_id' in validated_data:
            instance.reviewer = validated_data.pop('reviewer_id')

        return super().update(instance, validated_data)


class TaskAssignedOrReviewingSerializer(serializers.ModelSerializer):
    assignee = UserMiniSerializer(read_only=True)
    reviewer = UserMiniSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'board', 'title','description', 'status', 'priority', 'assignee', 'reviewer', 'due_date', 'comments_count']
    
    def get_comments_count(self, obj):
        return 0 # TODO Comments existieren noch nicht!
    

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
        read_only_fields = ['id']

    def get_author(self, obj):
        return obj.author.get_full_name() if obj.author else None


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    #author_id = serializers.IntegerField(source='author.id', read_only=True)
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
        read_only_fields = ['id', 'created_at']
    
    def get_author(self, obj):
        return obj.author.get_full_name()

