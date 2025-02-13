from django.utils.timezone import now


def check_if_due_today(frequency, last_completed, current_date=None):
    """ Проверка на необходимость выполнения действия сегодня """

    if current_date is None:
        current_date = now().date()

    if not last_completed:
        return True  # если ни разу не выполнялась, то нужно

    # Количество дней с момента последнего выполнения
    days_since_last = (current_date - last_completed).days

    return days_since_last >= frequency
