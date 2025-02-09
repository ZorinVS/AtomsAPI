from django.db import models

from habits import services
from users.models import User


class Habit(models.Model):
    """ Модель привычки """

    builder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits', verbose_name='habit_builder')
    location = models.CharField(max_length=255, verbose_name='location')
    time = models.TimeField(verbose_name='start time')
    action = models.CharField(max_length=255, verbose_name='action')
    is_enjoyable = models.BooleanField(default=False, verbose_name='is enjoyable')
    related_habit = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='related habit'
    )
    frequency = models.IntegerField(
        default=1, verbose_name='frequency (in days, 1 = daily, 2 = every 2 days, not more than 7 days)'
    )
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name='reward')
    time_required = models.IntegerField(verbose_name='required time (in seconds, maximum 120)')
    last_completed = models.DateField(blank=True, null=True, verbose_name='last completed')
    is_public = models.BooleanField(default=False, verbose_name='is public')

    def is_due_today(self):  # признак необходимости выполнения сегодня
        return services.check_if_due_today(self.frequency, self.last_completed)

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = 'habit'
        verbose_name_plural = 'habits'
        ordering = ('id',)
