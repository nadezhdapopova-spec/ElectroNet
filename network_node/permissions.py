from rest_framework.permissions import BasePermission


class IsActiveEmployee(BasePermission):
    def has_permission(self, request, view):
        """Является ли пользователь авторизованным и активным сотрудником"""
        return request.user.is_authenticated and request.user.is_active and request.user.is_staff
