from rest_framework import permissions

from core.models import User, Post, Comment


class IsUserOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: User) -> bool:
        return request.user == obj

class IsPostOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Post) -> bool:
        return request.user == obj.author

class IsCommentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Comment) -> bool:
        return request.user == obj.author
