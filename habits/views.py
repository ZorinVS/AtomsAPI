from django.db import models
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginators import HabitPagination
from habits.serializers import HabitSerializer
from users.permissions import IsOwnerOrReadOnly


class HabitViewSet(ModelViewSet):
    """ Операции CRUD модели `Habit` """

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = HabitPagination

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Habit.objects.none()
        if self.action == "list":
            return Habit.objects.filter(builder=self.request.user)
        return Habit.objects.filter(models.Q(builder=self.request.user) | models.Q(is_public=True))

    def perform_create(self, serializer):
        serializer.save(builder=self.request.user)

    @action(detail=False, methods=["get"], url_path="public")
    def list_public(self, request):
        """ Вывод только публичных привычек """

        queryset = Habit.objects.filter(is_public=True)  # публичные привычки

        paginated_queryset = self.paginate_queryset(queryset)
        if paginated_queryset:  # если пагинация возможна
            serializer = self.get_serializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'next': None,
            'previous': None,
            'results': serializer.data
        }, status=status.HTTP_200_OK)
