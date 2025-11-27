from rest_framework.permissions import BasePermission #, SAFE_METHODS
#from kanban_app.models import Board

# class ReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         return request.method in SAFE_METHODS
    
# class IsStaffOrReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         is_staff = bool(request.user and request.user.is_staff)
#         return is_staff or request.method in SAFE_METHODS
    
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    # -> Das Objekt selbst (zB Task, Board, Comment) hat ein Feld "owner". Es wird überprüft, ob dieses Objekt dem aktuellen Nutzer gehört.


class IsMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.members.filter(id=request.user.id).exists())


class IsBoardOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.board.owner == request.user)
    # -> Das Objekt gehört zu einem Board, besitzt ein Feld "board" (zB Task). Es wird überprüft, ob der Benutzer der Eigentümer des Boards ist, zu dem dieses Objekt gehört.


class IsBoardMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.board.members.filter(id=request.user.id).exists())
    # -> Das Objekt gehört zu einem Board, besitzt ein Feld "board" (zB Task). Es wird in der Many-to-Many-Relation "members" des Boards gesucht, ob der aktuelle User darin enthalten ist.
    
    
