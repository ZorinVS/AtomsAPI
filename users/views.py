from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.permissions import IsProfileOwner
from users.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """ Регистрация """

    serializer_class = UserSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    """ Обновление профиля """

    permission_classes = [IsAuthenticated, IsProfileOwner]
    serializer_class = UserSerializer
    queryset = User.objects.all()
