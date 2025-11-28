"""
Custom permission classes for the Kanmind API.

These permissions provide object-level access control for boards, tasks, and comments:
- IsBoardOwner: Grants access only to the owner of the associated board.
- IsBoardMember: Grants access to users who are members of the associated board.
- IsAuthor: Grants access only to the author of the object.
"""

from rest_framework.permissions import BasePermission


class IsBoardOwner(BasePermission):
    """
    Allows access only to the owner of the related board.

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


class IsBoardMember(BasePermission):
    """
    Allows access only to users who are members of the related board.

    Membership is checked through:
    - obj.members (Board)
    - obj.board.members (Task)
    - obj.task.board.members (Comment)
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'members'):
            return obj.members.filter(id=request.user.id).exists()
        elif hasattr(obj, 'board'):
            return obj.board.members.filter(id=request.user.id).exists()
        elif hasattr(obj, 'task'):
            return obj.task.board.members.filter(id=request.user.id).exists()
        return False
    
    
class IsAuthor(BasePermission):
    """
    Allows access only to the author of the object.

    Works for objects that define an 'author' field (Comment).
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
