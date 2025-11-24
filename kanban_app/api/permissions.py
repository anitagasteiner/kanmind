from rest_framework.permissions import BasePermission, SAFE_METHODS
from kanban_app.models import Board

# class ReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         return request.method in SAFE_METHODS
    
class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        is_staff = bool(request.user and request.user.is_staff)
        return is_staff or request.method in SAFE_METHODS
    
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_owner = bool(obj.owner == request.user)
        return is_owner


class IsBoardMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        board = obj.board
        return (
            request.user == board.owner or
            board.members.filter(id=request.user.id).exists()
        )
    