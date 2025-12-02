"""
Views for Kanmind Kanban Backend API.

This module contains API views for managing Boards, Tasks, and Comments.
Permissions are enforced to ensure that only board owners or members can access relevant resources, and authors can modify their own comments.

Views included:
- BoardsView: List and create boards for the current user.
- BoardDetail: Retrieve, update, or delete a specific board.
- EmailCheckView: Check if a user exists by email.
- TasksView: List all tasks or create a new task.
- TaskDetail: Retrieve, update, or delete a specific task.
- TasksAssignedToMeView: List tasks assigned to the current user.
- TasksReviewingView: List tasks where the current user is the reviewer.
- CommentsView: List or create comments for a task.
- CommentDetail: Retrieve or delete a specific comment.
"""

from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from kanban_app.models import Board, Task, Comment
from .serializers import TaskSerializer, BoardSerializer, BoardDetailSerializer, BoardUpdateSerializer, UserMiniSerializer, TaskAssignedOrReviewingSerializer, TaskCreateUpdateSerializer, CommentSerializer, CommentCreateUpdateSerializer
from .permissions import IsBoardOwner, IsBoardMember, IsAuthor


class BoardsView(generics.ListCreateAPIView):
    """
    List all boards that the current user owns or is a member of, 
    and allow creating new boards.
    """

    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsBoardOwner | IsBoardMember]

    def get_queryset(self):
        """Return boards where the user is owner or member."""
        user = self.request.user
        return Board.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()


class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific board by ID.
    """

    queryset = Board.objects.all()
    permission_classes = [IsAuthenticated, IsBoardOwner | IsBoardMember]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BoardUpdateSerializer
        return BoardDetailSerializer


class EmailCheckView(APIView):
    """
    Check if a user exists by their email address.
    """

    permission_classes = [IsAuthenticated] 
                          
    def get(self, request):
        """
        GET /auth/email-check/?email=<email>

        Args:
            request: DRF request object with query parameter 'email'.

        Returns:
            Response indicating whether the user exists and, if so, basic user info.
        """
                
        email = request.query_params.get('email')

        if not email:
            raise ValidationError({'email': 'Email parameter is required.'})
            # return Response(
            #     {"error": "Email parameter is required."},
            #     status=status.HTTP_400_BAD_REQUEST
            # )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"exists": False, "user": None},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = UserMiniSerializer(user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class TasksView(generics.ListCreateAPIView):
    """
    List all tasks and allow creation of new tasks.
    """
       
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsBoardOwner | IsBoardMember]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateUpdateSerializer
        return TaskSerializer


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific task.
    """
        
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsBoardOwner | IsBoardMember]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TaskCreateUpdateSerializer
        return TaskSerializer
    

class TasksAssignedToMeView(generics.ListAPIView):
    """
    List tasks assigned to the current user.
    """
        
    serializer_class = TaskAssignedOrReviewingSerializer
    permission_classes = [IsAuthenticated, IsBoardOwner | IsBoardMember]

    def get_queryset(self):
        """Return tasks where the current user is the assignee."""
        user = self.request.user
        return Task.objects.filter(assignee=user).distinct()
    

class TasksReviewingView(generics.ListAPIView):
    """
    List tasks where the current user is assigned as the reviewer.
    """
        
    serializer_class = TaskAssignedOrReviewingSerializer
    permission_classes = [IsAuthenticated, IsBoardOwner | IsBoardMember]

    def get_queryset(self):
        """Return tasks where the current user is the reviewer."""
        user = self.request.user
        return Task.objects.filter(reviewer=user).distinct()


class CommentsView(generics.ListCreateAPIView):
    """
    List comments for a specific task or create a new comment.
    """
        
    permission_classes = [IsAuthenticated, IsBoardOwner | IsBoardMember]
    
    def get_queryset(self):
        """Return comments related to the task identified by 'pk' URL parameter."""
        task_id = self.kwargs['pk']
        return Comment.objects.filter(task_id=task_id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateUpdateSerializer
        return  CommentSerializer

    def perform_create(self, serializer):
        """Set author to the current user and associate with the task."""
        serializer.save(
            author=self.request.user,
            task_id=self.kwargs['pk']
        )


class CommentDetail(generics.RetrieveDestroyAPIView): #generics.RetrieveUpdateDestroyAPIView
    """
    Retrieve or delete a specific comment.
    Additional object permission ensures only the author can delete their comment.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsBoardOwner | IsBoardMember]

    # def get_serializer_class(self):
    #     if self.request.method in ['PUT', 'PATCH']:
    #         return CommentCreateUpdateSerializer
    #     return CommentSerializer
    # -> Falls ich später möchte, dass der Author eines Comments diesen auch ändern kann, kann ich das hier noch nutzen!
    
    def get_queryset(self):
        """Return comments for the task identified by 'task_pk' URL parameter."""
        task_id = self.kwargs['task_pk']
        return Comment.objects.filter(task_id=task_id)
    
    def get_permissions(self):
        """
        Add IsAuthor permission for DELETE requests to ensure only comment authors can delete.
        """              
        permissions = super().get_permissions()
        if self.request.method == 'DELETE':
            permissions.append(IsAuthor())
        return permissions
    
