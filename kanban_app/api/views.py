from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated #, AllowAny
#from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.models import User
#from django.shortcuts import get_object_or_404
from kanban_app.models import Board, Task, Comment
from .serializers import TaskSerializer, BoardSerializer, BoardDetailSerializer, BoardUpdateSerializer, UserMiniSerializer, TaskAssignedOrReviewingSerializer, TaskCreateUpdateSerializer, CommentSerializer, CommentCreateUpdateSerializer
from .permissions import IsBoardOwner, IsBoardMember, IsAuthor


class BoardsView(generics.ListCreateAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsBoardOwner | IsBoardMember]

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()

class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    permission_classes = [IsBoardOwner | IsBoardMember]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BoardUpdateSerializer
        return BoardDetailSerializer

class EmailCheckView(APIView):
    permission_classes = [IsAuthenticated] 
                          
    def get(self, request):
        email = request.query_params.get('email')

        if not email:
            return Response(
                {"error": "Email parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"exists": False, "user": None},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = UserMiniSerializer(user)
        return Response(
            {"exists": True, "user": serializer.data},
            status=status.HTTP_200_OK
        )

class TasksView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    permission_classes = [IsBoardOwner | IsBoardMember]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateUpdateSerializer
        return TaskSerializer


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [IsBoardOwner | IsBoardMember]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TaskCreateUpdateSerializer
        return TaskSerializer
    

class TasksAssignedToMeView(generics.ListAPIView):
    serializer_class = TaskAssignedOrReviewingSerializer
    permission_classes = [IsBoardOwner | IsBoardMember]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignee=user).distinct()
    

class TasksReviewingView(generics.ListAPIView):
    serializer_class = TaskAssignedOrReviewingSerializer
    permission_classes = [IsBoardOwner | IsBoardMember]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(reviewer=user).distinct()


class CommentsView(generics.ListCreateAPIView):
    permission_classes = [IsBoardOwner | IsBoardMember]
    
    def get_queryset(self):
        task_id = self.kwargs['pk']
        return Comment.objects.filter(task_id=task_id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateUpdateSerializer
        return  CommentSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            task_id=self.kwargs['pk']
        )

class CommentDetail(generics.RetrieveDestroyAPIView): #generics.RetrieveUpdateDestroyAPIView
    serializer_class = CommentSerializer
    permission_classes = [IsBoardOwner | IsBoardMember]

    # def get_serializer_class(self):
    #     if self.request.method in ['PUT', 'PATCH']:
    #         return CommentCreateUpdateSerializer
    #     return CommentSerializer
    # -> Falls ich später möchte, dass der Author eines Comments diesen auch ändern kann, kann ich das hier noch nutzen!
    
    def get_queryset(self):
        task_id = self.kwargs['task_pk']
        return Comment.objects.filter(task_id=task_id)
    
    # zusätzliche Objekt-Permission für DELETE:
    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method == 'DELETE':
            permissions.append(IsAuthor())
        return permissions