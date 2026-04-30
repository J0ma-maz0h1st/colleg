from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Разрешает редактирование только владельцу профиля или администратору.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешаем, если пользователь — админ системы
        if request.user.is_staff:
            return True
        # Разрешаем, если пользователь — владелец этого профиля
        return obj.user == request.user