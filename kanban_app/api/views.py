from rest_framework import generics, status
from rest_framework.views import APIView
#from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.permissions import IsAuthenticated
#from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.models import User
#from django.shortcuts import get_object_or_404
from kanban_app.models import Board, Task
from .serializers import TaskSerializer, BoardSerializer, BoardDetailSerializer, BoardUpdateSerializer, UserMiniSerializer, TaskAssignedOrReviewingSerializer, TaskCreateSerializer
from .permissions import IsStaffOrReadOnly, IsOwner


class BoardsView(generics.ListCreateAPIView):
    #queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()

class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    permission_classes = [IsOwner]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BoardUpdateSerializer
        return BoardDetailSerializer

class EmailCheckView(APIView):
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

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer
    
    # def create(self, request, *args, **kwargs):
    #     serializer = self. get_serializer(data=request.data)
    #     if not serializer.is_valid():
    #         print(serializer.errors)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response(serializer.data, status=201)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
# class TaskViewSet(ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer

class TasksAssignedToMeView(generics.ListAPIView):
    serializer_class = TaskAssignedOrReviewingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignee=user).distinct()
    

class TasksReviewingView(generics.ListAPIView):
    serializer_class = TaskAssignedOrReviewingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(reviewer=user).distinct()
