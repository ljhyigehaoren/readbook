from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        message = "没有权限操作该对象"

        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user



