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
- gunicorn==23.0.0
- ipython 8.32.0
- pillow 11.1.0
- psycopg2-binary 2.9.10
- python-dotenv 1.0.1
- redis 5.2.1
- requests 2.32.3

## Локальный запуск
1. Клонирование репозитория
    ```shell
   git clone https://github.com/ZorinVS/AtomsAPI.git
   cd AtomsAPI
   git checkout feature/feature2
   ```
2. Создание `.env` файла из `.env.sample`
   - Копируйте файл
      ```shell
     cp .env.sample .env
     ```
   - Заполните файл данными
        ```shell
     nano .env
     ```
3. Запуск контейнеров
    ```shell
   docker-compose up -d --build
   ```
   Приложение будет доступно по адресу http://localhost.

## CI/CD

Проект настроен на автоматическое тестирование, сборку Docker-образов и деплой через GitHub Actions.

#### Workflow включает этапы:

1. Линтинг кода с использованием flake8
2. Запуск тестов (SQLite)
3. Сборка Docker-образов и публикация их на Docker Hub
4. Деплой на удаленный сервер

#### Настройка GitHub Secrets

В репозитории необходимо добавить следующие секреты:

- `DOCKER_HUB_USERNAME` — имя пользователя Docker Hub
- `DOCKER_HUB_ACCESS_TOKEN` — токен доступа Docker Hub
- `SSH_USER` — пользователь для SSH-подключения
- `SERVER_IP` — IP-адрес сервера
- `SSH_KEY` — приватный ключ для SSH-подключения
- `SECRET_KEY` — секретный ключ Django

## Настройка сервера

1. Установите Docker: [инструкция с официального сайта](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

2. Установите Docker Compose:
    ```shell
   sudo apt install docker-compose
   ```
3. Настройте файрвол:
    ```shell
   sudo ufw enable
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   ```
4. Установите Git:
    ```shell
   sudo apt install git
   ```
5. Клонируйте репозиторий с GitHub:
    ```shell
   sudo mkdir -p var/www
   cd var/www/
   git clone https://github.com/ZorinVS/AtomsAPI.git
   ```
6. Создайте файл `.env`:
   ```shell
   cd AtomsAPI
   git checkout feature/feature2
   sudo cp .env.sample .env
   sudo nano .env
   ```
7. Запуск контейнеров
    ```shell
   docker-compose up -d --build
   ```

## Адрес развернутого приложения
```plain
http://89.169.173.116
```
