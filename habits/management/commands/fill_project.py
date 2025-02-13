from django.core.management import BaseCommand, call_command

from users.models import User

FIXTURE_PATHS = (
    'users/fixtures/users_fixture.json',
    'habits/fixtures/habits_fixture.json',
)

AUTH_DETAILS = """
Данные для авторизации:
    - Администратор: james@example.com
    - Пользователь: user1@example.com
    - Пользователь: user2@example.com
    - 🔐: 123
"""


class Command(BaseCommand):
    help = 'Наполнение проекта тестовыми данными с выводом данных для авторизации'

    def handle(self, *args, **options):
        User.objects.all().delete()  # очистка БД перед загрузкой

        for fixture_path in FIXTURE_PATHS:  # загрузка данных
            call_command('loaddata', fixture_path)
        self.stdout.write(self.style.SUCCESS('Данные загружены успешно!'))
        self.stdout.write(AUTH_DETAILS)  # вывод данных для авторизации
