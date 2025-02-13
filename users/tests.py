from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):

    def setUp(self):
        """ Подготовка тестовых данных """

        self.orm_data = [
            {
                'email': 'test1@test.com',
            },
            {
                'email': 'test2@test.com',
                'telegram_id': '987654321',
            },
            {
                'email': 'test3@test.com',
            }
        ]
        self.pw = {'password': '123'}
        User.objects.create(**self.orm_data[0])
        self.user = User.objects.create_user(**self.orm_data[2], **self.pw)

    def test_bad_request_create_user(self):
        """ Тест создания пользователем с почтой, которая уже занята """

        url = reverse('users:users-create')
        response = self.client.post(url, data={**self.orm_data[0], **self.pw})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()['email'][0],
            'user with this email already exists.',
        )

    def test_successfully_create_user(self):
        """ Тест успешной регистрации """

        url = reverse('users:users-create')
        response = self.client.post(url, data={**self.orm_data[1], **self.pw})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, expected in self.orm_data[1].items():
            self.assertEqual(
                response.json()[key],
                expected,
            )

    def test_update_user(self):
        """ Тест обновления профиля """

        url = reverse('users:users-update', kwargs={'pk': self.user.pk})
        self.client.force_authenticate(user=self.user)
        data_for_update = {'telegram_id': '123456789'}
        response = self.client.patch(url, data=data_for_update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key, expected in {**self.orm_data[2], **data_for_update}.items():
            self.assertEqual(
                response.json()[key],
                expected,
            )
