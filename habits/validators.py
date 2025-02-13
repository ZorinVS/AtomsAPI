from rest_framework import serializers


class RelatedHabitOrRewardValidator:
    """ Валидация для исключения одновременного указания связанной привычки и вознаграждения """

    def __call__(self, values):
        if values.get('related_habit') and values.get('reward'):
            raise serializers.ValidationError('A habit cannot have both a related habit and a reward at the same time')


def validate_execution_time(value):
    """ Валидация времени выполнения привычки (не более 120 сек.) """

    if value < 1 or value > 120:
        raise serializers.ValidationError('Execution time must not exceed 120 seconds'
                                          if value > 0 else 'Execution time cannot be negative')


def validate_related_habit(habit):
    """ Валидация связанной привычки, которая должна быть приятной """

    if habit and not habit.is_enjoyable:
        raise serializers.ValidationError('The related habit must be an enjoyable habit')


class EnjoyableHabitValidator:
    """ Валидация на отсутствие связанной привычки или вознаграждения у приятной привычки """

    def __call__(self, values):
        if values.get('is_enjoyable') and (values.get('related_habit') or values.get('reward')):
            raise serializers.ValidationError('An enjoyable habit cannot have a reward or a related habit')


def validate_frequency(value):
    """ Валидация частоты выполнения привычки (не реже чем один раз в неделю) """

    if value < 1 or value > 7:
        raise serializers.ValidationError('A habit must be performed at least once every 7 days')
