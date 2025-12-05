"""
Custom permission classes for the Kanmind API.

These permissions provide object-level access control for boards, tasks, and comments:
- IsBoardOwnerOrMember: Grants access only to users who are the owner or a member of the associated board.
- IsBoardOwner: Grants access only to users who are the owner of the associated board.
- IsAuthor: Grants access only to the author of the object.
"""

from rest_framework.permissions import BasePermission


class IsBoardOwnerOrMember(BasePermission):
    """
    Allows access only to users who are the owner or a member of the related board.

    This permission handles different object types by resolving ownership through:
    - obj.owner (Board)
    - obj.members (Board)
    - obj.board.owner (Task)
    - obj.board.members (Task)
    - obj.task.board.owner (Comment)
    - obj.task.board.members (Comment)
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'members'):
            return obj.members.filter(id=request.user.id).exists()
        elif hasattr(obj, 'board'):
            if obj.board.owner == request.user or obj.board.members.filter(id=request.user.id).exists():
                return True
        elif hasattr(obj, 'task'):
            if obj.task.board.owner == request.user or obj.task.board.members.filter(id=request.user.id).exists():
                return True
        return False
    
    
class IsBoardOwner(BasePermission):
    """ Allows access only to the owner of the related board.
    
    This permission handles different object types by resolving ownership through:
    - obj.owner (Board)
    - obj.board.owner (Task)
    - obj.task.board.owner (Comment)
    """
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'board'):
            return obj.board.owner == request.user
        elif hasattr(obj, 'task'):
            return obj.task.board.owner == request.user
        return False


class IsAuthor(BasePermission):
    """
    Allows access only to the author of the object.

    Works for objects that define an 'author' field (Comment).
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
