from rest_framework import permissions

class IsMentorOrAdmin(permissions.BasePermission):
    """
    Разрешает доступ только наставникам или администраторам.
    """
    def has_permission(self, request, view):
        # Разрешаем, если пользователь — админ системы
        if request.user.is_staff:
            return True
        # Разрешаем, если пользователь — наставник
        return hasattr(request.user, 'mentor')