from rest_framework import permissions

class IsMentorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.role in ['mentor', 'admin'] or request.user.is_staff)
        )

class IsStudent(permissions.BasePermission):
    """Разрешает доступ только пользователям с ролью 'student'."""
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'student'
        )