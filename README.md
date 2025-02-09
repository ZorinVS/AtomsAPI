# AtomsAPI

## Описание
**AtomsAPI** – это серверная часть SPA веб-приложения для отслеживания полезных привычек, 
основанная на концепции, изложенной в книге Джеймса Клира «Атомные привычки». 
Проект позволяет пользователям добавлять, редактировать и удалять привычки, получать напоминания в Telegram.

## Зависимости
- celery 5.4.0 
- coverage 7.6.11
- Django 5.1.5 
- django-celery-beat 2.7.0
- django-cors-headers 4.6.0
- djangorestframework 3.15.2
- djangorestframework_simplejwt 5.4.0
- drf-yasg 1.21.8
- flake8 7.1.1
- ipython 8.32.0
- pillow 11.1.0
- psycopg2-binary 2.9.10
- python-dotenv 1.0.1
- redis 5.2.1
- requests 2.32.3

## Установка
1. Клонируйте репозиторий:
   ```shell
   git clone git@github.com:ZorinVS/AtomsAPI.git
   ```
2. Установите зависимости:
   ```shell
   pip3 install -r requirements.txt
   ```

## Подключение БД
1. Создайте БД
2. Создайте файл `.env` из файла `.env.sample`

## Применение миграций
```shell
python manage.py migrate
```

## Наполнение проекта данными
```shell
python3 manage.py fill_project
```

## Запуск
1. Запустите сервер Django:
   ```shell
   python3 manage.py runserver
   ```
2. Запустите брокер Redis:
   ```shell
   redis-server
   ```
3. Запустите Celery worker с планировщиком Celery beat:
   ```shell
   celery -A config worker --beat --scheduler django --loglevel=info
   ```

## Тестирование
Создание текстового отчёта:
```shell
coverage run --source='.' --omit='*/migrations/*','*/management/*','*/__init__.py' manage.py test && coverage report
```
#### Результат запуска тестов
| Name                     | Stmts | Miss | Cover |
|--------------------------|------:|-----:|------:|
| config/asgi.py           |     4 |    4 |    0% |
| config/celery.py         |     7 |    0 |  100% |
| config/settings.py       |    38 |    0 |  100% |
| config/urls.py           |    11 |    1 |   91% |
| config/wsgi.py           |     4 |    4 |    0% |
| habits/admin.py          |     6 |    0 |  100% |
| habits/apps.py           |     4 |    0 |  100% |
| habits/models.py         |    23 |    2 |   91% |
| habits/paginators.py     |     5 |    0 |  100% |
| habits/serializers.py    |    12 |    0 |  100% |
| habits/services.py       |     8 |    6 |   25% |
| habits/tests.py          |   103 |    0 |  100% |
| habits/urls.py           |     7 |    0 |  100% |
| habits/validators.py     |    18 |    0 |  100% |
| habits/views.py          |    31 |    3 |   90% |
| manage.py                |    11 |    2 |   82% |
| users/admin.py           |     6 |    0 |  100% |
| users/apps.py            |     4 |    0 |  100% |
| users/models.py          |    33 |    9 |   73% |
| users/permissions.py     |    11 |    0 |  100% |
| users/serializers.py     |    19 |    1 |   95% |
| users/services.py        |    25 |   25 |    0% |
| users/tasks.py           |    12 |   12 |    0% |
| users/tests.py           |    29 |    0 |  100% |
| users/urls.py            |     6 |    0 |  100% |
| users/views.py           |    11 |    0 |  100% |
| **TOTAL**                |   448 |   69 |   85% |
