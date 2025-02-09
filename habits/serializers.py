from rest_framework import serializers

from habits.models import Habit
from habits.validators import (
    EnjoyableHabitValidator,
    RelatedHabitOrRewardValidator,
    validate_execution_time,
    validate_frequency,
    validate_related_habit,
)


class HabitSerializer(serializers.ModelSerializer):
    """ Сериализация для модели `Habit` """

    frequency = serializers.IntegerField(validators=[validate_frequency])
    time_required = serializers.IntegerField(validators=[validate_execution_time])
    related_habit = serializers.PrimaryKeyRelatedField(
        queryset=Habit.objects.all(), required=False, allow_null=True, validators=[validate_related_habit]
    )

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('builder',)
        validators = [
            EnjoyableHabitValidator(),
            RelatedHabitOrRewardValidator(),
        ]
