from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        """ Подготовка тестовых данных """

        self.orm_data = (
            {
                'location': 'Дом',
                'time': '19:10:00',
                'action': 'Растяжка',
                'is_enjoyable': False,
                'frequency': 1,
                'reward': 'Просмотр netflix',
                'time_required': 120,
                'is_public': True
            },
            {
                'location': 'Дом',
                'time': '19:30:00',
                'action': 'Собраться на тренировку',
                'is_enjoyable': True,
                'frequency': 2,
                'time_required': 120,
                'is_public': True
            },
        )
        self.users = []
        self.habits = []

        for i, habit_data in enumerate(self.orm_data):
            user = User.objects.create(email=f'user{i}@test.com')
            habit = Habit.objects.create(**habit_data, builder=user)

            self.users.append(user)
            self.habits.append(habit)

    def test_forbidden_create_habit(self):
        """ Тест создания неавторизованным пользователем """

        url = reverse('habits:habit-list')
        response = self.client.post(url, data=self.orm_data[1])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_successfully_create_habit(self):
        """ Тест успешного создания """

        url = reverse('habits:habit-list')
        self.client.force_authenticate(user=self.users[0])
        response = self.client.post(url, data=self.orm_data[1])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['action'], self.orm_data[1]['action'])
        self.assertEqual(response.json()['builder'], self.users[0].pk)

    def test_create_habit_with_related_habit_and_reward(self):
        """ Тест создания с одновременным указанием связанной привычки и вознаграждения """

        url = reverse('habits:habit-list')
        related_habit = {'related_habit': self.habits[1].pk}
        self.client.force_authenticate(user=self.users[1])
        response = self.client.post(
            path=url,
            data={**self.orm_data[0], **related_habit},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.json())
        self.assertEqual(
            response.json()['non_field_errors'][0],
            'A habit cannot have both a related habit and a reward at the same time'
        )

    def test_create_habit_with_wrong_execution_time(self):
        """ Тест создания с некорректным временем выполнения """

        url = reverse('habits:habit-list')
        wrong_execution_time = {'time_required': 121}
        self.client.force_authenticate(user=self.users[1])
        response = self.client.post(
            path=url,
            data={**self.orm_data[0], **wrong_execution_time},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()['time_required'][0],
            'Execution time must not exceed 120 seconds'
        )

    def test_create_habit_with_wrong_related_habit(self):
        """ Тест создания со связанной привычкой, которая не является приятной """

        url = reverse('habits:habit-list')
        related_habit = {'related_habit': self.habits[0].pk}
        self.client.force_authenticate(user=self.users[0])
        response = self.client.post(url, data={**self.orm_data[1], **related_habit})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()['related_habit'][0],
            'The related habit must be an enjoyable habit'
        )

    def test_unsuccessfully_create_enjoyable_habit(self):
        """ Тест создания приятной привычки, которая содержит вознаграждение """

        url = reverse('habits:habit-list')
        reward = {'reward': 'Просмотр netflix'}
        self.client.force_authenticate(user=self.users[0])
        response = self.client.post(url, data={**self.orm_data[1], **reward})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()['non_field_errors'][0],
            'An enjoyable habit cannot have a reward or a related habit'
        )

    def test_create_habit_with_wrong_frequency(self):
        """ Тест создания с частотой выполнения реже, чем раз в неделю """

        url = reverse('habits:habit-list')
        wrong_frequency = {'frequency': 8}
        self.client.force_authenticate(user=self.users[1])
        response = self.client.post(url, data={**self.orm_data[0], **wrong_frequency})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()['frequency'][0],
            'A habit must be performed at least once every 7 days'
        )

    def test_get_list_habit(self):
        """ Тест получения списка пользователя """

        url = reverse('habits:habit-list')
        self.client.force_authenticate(user=self.users[0])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

    def test_get_list_public_habit(self):
        """ Тест получения списка публичных привычек """

        url = reverse('habits:habit-list-public')
        self.client.force_authenticate(user=self.users[0])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 2)

    def test_get_habit_detail(self):
        """ Тест получения детальной информации """

        url = reverse('habits:habit-detail', kwargs={'pk': self.habits[0].pk})
        self.client.force_authenticate(user=self.users[0])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key, expected in self.orm_data[0].items():
            result = response.json()[key]
            if isinstance(expected, str):  # '19:10' in '19:10:00'
                self.assertIn(result, expected)
            else:
                self.assertEqual(expected, result)

    def test_successfully_update_habit(self):
        """ Тест успешного обновления привычки """

        url = reverse('habits:habit-detail', kwargs={'pk': self.habits[0].pk})
        data_for_update = {'frequency': 3}
        self.client.force_authenticate(user=self.users[0])
        response = self.client.patch(url, data=data_for_update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['frequency'], data_for_update['frequency'])

    def test_update_stranger_habit(self):
        """ Тест обновления чужой привычки """

        url = reverse('habits:habit-detail', kwargs={'pk': self.habits[1].pk})
        data_for_update = {'frequency': 3}
        self.client.force_authenticate(user=self.users[0])
        response = self.client.patch(url, data=data_for_update)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['detail'], "This habit wasn't created by you!")

    def test_delete_habit(self):
        """ Тест удаления привычки """

        url = reverse('habits:habit-detail', kwargs={'pk': self.habits[0].pk})
        self.client.force_authenticate(user=self.users[0])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
