from celery import shared_task

from users import services
from users.models import User


@shared_task
def send_reminder_tg_message():
    users = User.objects.exclude(telegram_id=None)
    for user in users:
        print(user)
        habits, current_time = services.get_user_habits_to_remind(user).values()
        for reminder_data in services.get_text_messages_with_tg_id(habits, current_time):
            print('Данные для отправки:', reminder_data)
            services.send_telegram_message(**reminder_data)
