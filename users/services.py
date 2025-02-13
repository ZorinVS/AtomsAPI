from datetime import timedelta

import requests
from django.db.models import Q
from django.utils.timezone import now, localtime

from config import settings

REMINDER_TIME = 15  # время (в минутах) до выполнения привычки


def send_telegram_message(chat_id, message):
    """ Отправка сообщения через телеграм бот """

    params = {'text': message, 'chat_id': chat_id}
    requests.get(f'{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage', params=params)


def get_user_habits_to_remind(user):
    """ Получение привычек пользователя, о которых необходимо напомнить """

    current_time = localtime(now()).time()
    reminder_time = (localtime(now() + timedelta(minutes=REMINDER_TIME))).time()

    reminded_habits = user.habits.filter(
        Q(time__hour=current_time.hour, time__minute=current_time.minute) |
        Q(time__hour=reminder_time.hour, time__minute=reminder_time.minute)
    )

    return {
        'habits': [habit for habit in reminded_habits if habit.is_due_today()],
        'current_time': current_time,
    }


def get_text_messages_with_tg_id(habits, current_time):
    """ Получение данных для отправки напоминания """

    if not habits:
        return []

    user_id = habits[0].builder.telegram_id
    text_with_telegram_id = []
    for habit in habits:
        tg_data = {
            'chat_id': user_id,
            'message': f"Пора приступить к выполнению привычки '{habit.action.capitalize()}'!",
        }
        if habit.time.hour != current_time.hour or habit.time.minute != current_time.minute:
            tg_data['message'] = tg_data['message'].replace('Пора', f'Через {REMINDER_TIME} минут будет пора')
        text_with_telegram_id.append(tg_data)
    return text_with_telegram_id
