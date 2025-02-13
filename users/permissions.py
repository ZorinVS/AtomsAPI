from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """ Полный доступ дается только создателю привычки """

    message = "This habit wasn't created by you!"

    def has_object_permission(self, request, view, obj):
        """ Проверка прав доступа к объекту:
            - Изменение и удаление доступно только создателю привычки
            - Чтение доступно для публичных привычек или своих привычек
        """

        if request.method in SAFE_METHODS:  # чтение
            return obj.is_public or request.user == obj.builder

        return obj.builder == request.user


class IsProfileOwner(permissions.BasePermission):
    """ Проверка на владельца профиля """

    def has_object_permission(self, request, view, obj):
        return request.user == obj
